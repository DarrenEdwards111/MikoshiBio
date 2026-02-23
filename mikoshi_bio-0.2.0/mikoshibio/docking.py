"""
Molecular Docking Tools for MikoshiLang
AutoDock Vina integration for protein-ligand docking.
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import tempfile
import subprocess

try:
    from vina import Vina
    VINA_AVAILABLE = True
except ImportError:
    VINA_AVAILABLE = False


def DockLigand(receptor_pdbqt: str, ligand_pdbqt: str, 
               center: Tuple[float, float, float],
               box_size: Tuple[float, float, float] = (20.0, 20.0, 20.0),
               exhaustiveness: int = 8,
               n_poses: int = 9) -> List[Dict[str, Any]]:
    """
    Dock ligand to receptor using AutoDock Vina.
    
    Args:
        receptor_pdbqt: Path to receptor PDBQT file
        ligand_pdbqt: Path to ligand PDBQT file
        center: Docking box center (x, y, z) in Angstroms
        box_size: Docking box dimensions (x, y, z) in Angstroms
        exhaustiveness: Vina exhaustiveness parameter (default 8)
        n_poses: Number of binding poses to generate
    
    Returns:
        List of docking poses with affinity scores
    """
    if not VINA_AVAILABLE:
        raise ImportError("Vina not installed. Install with: pip install vina")
    
    v = Vina(sf_name='vina')
    
    # Set receptor
    v.set_receptor(receptor_pdbqt)
    
    # Set ligand
    v.set_ligand_from_file(ligand_pdbqt)
    
    # Compute Vina maps
    v.compute_vina_maps(center=center, box_size=box_size)
    
    # Dock
    v.dock(exhaustiveness=exhaustiveness, n_poses=n_poses)
    
    # Get results
    energies = v.energies()
    
    results = []
    for i, (affinity, lb_rmsd, ub_rmsd) in enumerate(energies):
        results.append({
            "pose": i + 1,
            "affinity": float(affinity),  # kcal/mol
            "rmsd_lb": float(lb_rmsd),
            "rmsd_ub": float(ub_rmsd),
        })
    
    return results


def CalculateBindingAffinity(receptor_pdbqt: str, ligand_pdbqt: str,
                             center: Tuple[float, float, float],
                             box_size: Tuple[float, float, float] = (20.0, 20.0, 20.0)) -> float:
    """
    Calculate binding affinity (best docking score).
    
    Returns:
        Binding affinity in kcal/mol (negative = favorable)
    """
    results = DockLigand(receptor_pdbqt, ligand_pdbqt, center, box_size, n_poses=1)
    return results[0]["affinity"]


def SaveDockingPoses(receptor_pdbqt: str, ligand_pdbqt: str,
                     center: Tuple[float, float, float],
                     output_path: str,
                     box_size: Tuple[float, float, float] = (20.0, 20.0, 20.0),
                     n_poses: int = 9) -> List[Dict[str, Any]]:
    """
    Dock ligand and save poses to PDBQT file.
    
    Args:
        receptor_pdbqt: Receptor file
        ligand_pdbqt: Ligand file
        center: Box center
        output_path: Output PDBQT file for poses
        box_size: Box dimensions
        n_poses: Number of poses
    
    Returns:
        List of pose energies
    """
    if not VINA_AVAILABLE:
        raise ImportError("Vina not installed")
    
    v = Vina(sf_name='vina')
    v.set_receptor(receptor_pdbqt)
    v.set_ligand_from_file(ligand_pdbqt)
    v.compute_vina_maps(center=center, box_size=box_size)
    v.dock(exhaustiveness=8, n_poses=n_poses)
    
    # Write output
    v.write_poses(output_path, n_poses=n_poses, overwrite=True)
    
    # Return energies
    energies = v.energies()
    return [{
        "pose": i + 1,
        "affinity": float(aff),
        "rmsd_lb": float(lb),
        "rmsd_ub": float(ub),
    } for i, (aff, lb, ub) in enumerate(energies)]


def ConvertPDBtoPDBQT(pdb_file: str, output_pdbqt: Optional[str] = None,
                      is_receptor: bool = False) -> str:
    """
    Convert PDB to PDBQT using OpenBabel or MGLTools.
    
    Args:
        pdb_file: Input PDB file
        output_pdbqt: Output PDBQT file (optional, auto-generated)
        is_receptor: True for protein receptor, False for ligand
    
    Returns:
        Path to generated PDBQT file
    """
    if output_pdbqt is None:
        base = os.path.splitext(pdb_file)[0]
        output_pdbqt = f"{base}.pdbqt"
    
    try:
        # Try OpenBabel first
        cmd = [
            "obabel",
            pdb_file,
            "-O", output_pdbqt,
            "-p", "7.4"  # pH
        ]
        
        if not is_receptor:
            cmd.extend(["--gen3d"])  # Generate 3D for ligands
        
        subprocess.run(cmd, check=True, capture_output=True)
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: try MGLTools prepare scripts
        try:
            if is_receptor:
                cmd = ["prepare_receptor4.py", "-r", pdb_file, "-o", output_pdbqt]
            else:
                cmd = ["prepare_ligand4.py", "-l", pdb_file, "-o", output_pdbqt]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "Could not convert PDB to PDBQT. Install either:\n"
                "  - OpenBabel: conda install -c conda-forge openbabel\n"
                "  - MGLTools: https://ccsb.scripps.edu/mgltools/"
            )
    
    return output_pdbqt


def CalculateBoxFromBindingSite(receptor_pdb: str, ligand_residue: str,
                                 padding: float = 10.0) -> Tuple[Tuple[float, float, float], 
                                                                 Tuple[float, float, float]]:
    """
    Calculate docking box from known binding site ligand.
    
    Args:
        receptor_pdb: PDB file with receptor and bound ligand
        ligand_residue: Residue name of ligand (e.g., "ATP")
        padding: Extra space around ligand (Angstroms)
    
    Returns:
        Tuple of (center, box_size)
    """
    from Bio.PDB import PDBParser
    import numpy as np
    
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("receptor", receptor_pdb)
    
    # Find ligand atoms
    ligand_coords = []
    for residue in structure.get_residues():
        if residue.get_resname() == ligand_residue:
            for atom in residue.get_atoms():
                ligand_coords.append(atom.coord)
    
    if not ligand_coords:
        raise ValueError(f"Ligand {ligand_residue} not found in {receptor_pdb}")
    
    coords = np.array(ligand_coords)
    
    # Calculate bounding box
    min_coords = coords.min(axis=0)
    max_coords = coords.max(axis=0)
    
    center = tuple((min_coords + max_coords) / 2)
    box_size = tuple(max_coords - min_coords + padding)
    
    return center, box_size


def VirtualScreening(receptor_pdbqt: str, ligand_library: List[str],
                     center: Tuple[float, float, float],
                     box_size: Tuple[float, float, float] = (20.0, 20.0, 20.0),
                     top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Virtual screening: dock multiple ligands and rank by affinity.
    
    Args:
        receptor_pdbqt: Receptor PDBQT file
        ligand_library: List of ligand PDBQT file paths
        center: Docking box center
        box_size: Docking box size
        top_n: Number of top hits to return
    
    Returns:
        List of top N ligands sorted by affinity
    """
    if not VINA_AVAILABLE:
        raise ImportError("Vina not installed")
    
    v = Vina(sf_name='vina')
    v.set_receptor(receptor_pdbqt)
    v.compute_vina_maps(center=center, box_size=box_size)
    
    results = []
    
    for ligand_file in ligand_library:
        try:
            v.set_ligand_from_file(ligand_file)
            v.dock(exhaustiveness=8, n_poses=1)
            
            energy = v.energies()[0][0]  # Best pose affinity
            
            results.append({
                "ligand": os.path.basename(ligand_file),
                "affinity": float(energy),
                "path": ligand_file,
            })
        except Exception as e:
            print(f"Warning: Failed to dock {ligand_file}: {e}")
            continue
    
    # Sort by affinity (most negative = best)
    results.sort(key=lambda x: x["affinity"])
    
    return results[:top_n]


# Export all functions
__all__ = [
    "DockLigand",
    "CalculateBindingAffinity",
    "SaveDockingPoses",
    "ConvertPDBtoPDBQT",
    "CalculateBoxFromBindingSite",
    "VirtualScreening",
]
