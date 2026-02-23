"""
BioPython Integration for MikoshiLang
Wrapper for Bio.PDB, Bio.Seq, and other BioPython modules.
"""

from typing import List, Dict, Any, Optional, Tuple
import io
import requests
from Bio.PDB import PDBParser, PDBIO, Select, NeighborSearch
from Bio.PDB.Polypeptide import PPBuilder
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight
import numpy as np


def LoadPDB(source: str, pdb_id: Optional[str] = None) -> Any:
    """
    Load PDB structure from file path, URL, or PDB ID.
    
    Args:
        source: File path, URL, or "pdb" for PDB ID lookup
        pdb_id: PDB ID if source="pdb"
    
    Returns:
        Bio.PDB.Structure object
    """
    parser = PDBParser(QUIET=True)
    
    if source == "pdb" and pdb_id:
        # Download from PDB
        url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
        response = requests.get(url, timeout=30)
        structure = parser.get_structure(pdb_id, io.StringIO(response.text))
    elif source.startswith("http"):
        # Download from URL
        response = requests.get(source, timeout=30)
        structure = parser.get_structure("structure", io.StringIO(response.text))
    else:
        # Load from file
        structure = parser.get_structure("structure", source)
    
    return structure


def GetSequence(structure: Any, chain_id: Optional[str] = None) -> str:
    """Extract amino acid sequence from structure."""
    ppb = PPBuilder()
    
    sequences = []
    for chain in structure.get_chains():
        if chain_id and chain.id != chain_id:
            continue
        for pp in ppb.build_peptides(chain):
            sequences.append(str(pp.get_sequence()))
    
    return "".join(sequences)


def FindContacts(structure: Any, distance: float = 5.0, chain1: Optional[str] = None, 
                 chain2: Optional[str] = None) -> List[Tuple[Any, Any, float]]:
    """
    Find inter-atomic contacts within distance threshold.
    
    Returns:
        List of (atom1, atom2, distance) tuples
    """
    atoms = []
    for chain in structure.get_chains():
        if chain1 and chain.id == chain1:
            atoms.extend(list(chain.get_atoms()))
        elif chain2 and chain.id == chain2:
            atoms.extend(list(chain.get_atoms()))
        elif not chain1 and not chain2:
            atoms.extend(list(chain.get_atoms()))
    
    ns = NeighborSearch(atoms)
    contacts = ns.search_all(distance, level='A')  # Atom level
    
    return [(a1, a2, (a1 - a2)) for a1, a2 in contacts]


def CalculateRMSD(structure1: Any, structure2: Any, chain_id: Optional[str] = None) -> float:
    """
    Calculate RMSD between two structures.
    
    Args:
        structure1: Reference structure
        structure2: Mobile structure
        chain_id: Specific chain to compare (optional)
    
    Returns:
        RMSD in Angstroms
    """
    from Bio.PDB import Superimposer
    
    # Get CA atoms
    atoms1 = []
    atoms2 = []
    
    for chain in structure1.get_chains():
        if chain_id and chain.id != chain_id:
            continue
        for residue in chain:
            if residue.has_id('CA'):
                atoms1.append(residue['CA'])
    
    for chain in structure2.get_chains():
        if chain_id and chain.id != chain_id:
            continue
        for residue in chain:
            if residue.has_id('CA'):
                atoms2.append(residue['CA'])
    
    if len(atoms1) != len(atoms2):
        raise ValueError(f"Structure mismatch: {len(atoms1)} vs {len(atoms2)} CA atoms")
    
    super_imposer = Superimposer()
    super_imposer.set_atoms(atoms1, atoms2)
    
    return super_imposer.rms


def CalculateSecondaryStructure(structure: Any, pdb_file: str) -> Dict[str, Any]:
    """
    Calculate secondary structure using DSSP.
    
    Args:
        structure: Bio.PDB.Structure
        pdb_file: Path to PDB file (required by DSSP)
    
    Returns:
        Dict with secondary structure assignments
    """
    try:
        from Bio.PDB.DSSP import DSSP
        
        model = structure[0]
        dssp = DSSP(model, pdb_file)
        
        ss_data = {}
        for key in dssp:
            chain_id, residue_id = key
            ss_code = dssp[key][2]  # Secondary structure code
            
            if chain_id not in ss_data:
                ss_data[chain_id] = []
            
            ss_data[chain_id].append({
                "residue": residue_id[1],
                "ss": ss_code,
                "acc": dssp[key][3],  # Accessibility
                "phi": dssp[key][4],  # Phi angle
                "psi": dssp[key][5],  # Psi angle
            })
        
        return ss_data
    except Exception as e:
        return {"error": str(e), "note": "DSSP requires dssp binary installed"}


def GetBindingSites(structure: Any, ligand_name: str, distance: float = 4.0) -> List[Any]:
    """
    Find protein residues near a ligand.
    
    Args:
        structure: Bio.PDB.Structure
        ligand_name: Ligand residue name (e.g., "ATP", "HEM")
        distance: Contact distance in Angstroms
    
    Returns:
        List of residues in contact with ligand
    """
    # Find ligand atoms
    ligand_atoms = []
    for residue in structure.get_residues():
        if residue.get_resname() == ligand_name:
            ligand_atoms.extend(list(residue.get_atoms()))
    
    if not ligand_atoms:
        return []
    
    # Find nearby protein atoms
    protein_atoms = []
    for chain in structure.get_chains():
        for residue in chain:
            if residue.id[0] == ' ':  # Standard amino acid
                protein_atoms.extend(list(residue.get_atoms()))
    
    ns = NeighborSearch(protein_atoms + ligand_atoms)
    
    binding_residues = set()
    for lig_atom in ligand_atoms:
        nearby = ns.search(lig_atom.coord, distance, level='R')
        for residue in nearby:
            if residue.id[0] == ' ':  # Exclude ligands
                binding_residues.add(residue)
    
    return list(binding_residues)


def SequenceAnalysis(sequence: str) -> Dict[str, Any]:
    """
    Analyze protein sequence properties.
    
    Returns:
        Dict with molecular weight, isoelectric point, composition
    """
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    
    seq = Seq(sequence)
    analysis = ProteinAnalysis(str(seq))
    
    return {
        "length": len(sequence),
        "molecular_weight": analysis.molecular_weight(),
        "aromaticity": analysis.aromaticity(),
        "instability_index": analysis.instability_index(),
        "isoelectric_point": analysis.isoelectric_point(),
        "secondary_structure_fraction": analysis.secondary_structure_fraction(),
        "amino_acid_percent": analysis.get_amino_acids_percent(),
    }


# Export all functions
__all__ = [
    "LoadPDB",
    "GetSequence",
    "FindContacts",
    "CalculateRMSD",
    "CalculateSecondaryStructure",
    "GetBindingSites",
    "SequenceAnalysis",
]
