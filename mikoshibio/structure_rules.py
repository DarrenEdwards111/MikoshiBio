"""
MikoshiLang Integration Rules for MikoshiBio

Makes BioPython functions callable in Wolfram-style syntax:
  LoadPDB["pdb", "1CRN"]
  GetSequence[structure]
  FindContacts[structure, 5.0]

Note: Requires MikoshiLang to be installed.
Install with: pip install mikoshi-bio[symbolic]
"""

try:
    from mikoshilang.rules import RuleDelayed
    from mikoshilang.expr import Expr
    MIKOSHILANG_AVAILABLE = True
except ImportError:
    MIKOSHILANG_AVAILABLE = False
    RuleDelayed = None
    Expr = None

from .pdb_pack import PDBPack
from . import biopython_bridge as bio


# Initialize PDB pack
_pdb_pack = PDBPack()


def pack_search_pdb(query, limit=5):
    """PackSearch["pdb", query] integration."""
    return _pdb_pack.search(query, limit)


def pack_value_pdb(pdb_id, property, **kwargs):
    """PackValue["pdb", id, property] integration."""
    return _pdb_pack.get_value(pdb_id, property, **kwargs)


def load_pdb_rule(source, pdb_id=None):
    """LoadPDB["pdb", "1CRN"] or LoadPDB["/path/to/file.pdb"]"""
    if source == "pdb" and pdb_id:
        return bio.LoadPDB("pdb", pdb_id)
    return bio.LoadPDB(source)


def get_sequence_rule(structure, chain_id=None):
    """GetSequence[structure] or GetSequence[structure, "A"]"""
    return bio.GetSequence(structure, chain_id)


def find_contacts_rule(structure, distance=5.0, chain1=None, chain2=None):
    """FindContacts[structure, 5.0]"""
    contacts = bio.FindContacts(structure, distance, chain1, chain2)
    # Return simplified format
    return [
        {
            "atom1": str(c[0]),
            "atom2": str(c[1]),
            "distance": float(c[2]),
        }
        for c in contacts[:100]  # Limit to 100 contacts for display
    ]


def calculate_rmsd_rule(structure1, structure2, chain_id=None):
    """CalculateRMSD[struct1, struct2]"""
    return bio.CalculateRMSD(structure1, structure2, chain_id)


def secondary_structure_rule(structure, pdb_file):
    """CalculateSecondaryStructure[structure, "file.pdb"]"""
    return bio.CalculateSecondaryStructure(structure, pdb_file)


def binding_sites_rule(structure, ligand_name, distance=4.0):
    """GetBindingSites[structure, "ATP"]"""
    residues = bio.GetBindingSites(structure, ligand_name, distance)
    return [
        {
            "residue": res.get_resname(),
            "number": res.id[1],
            "chain": res.get_parent().id,
        }
        for res in residues
    ]


def sequence_analysis_rule(sequence):
    """SequenceAnalysis["MVHLTPEEK..."]"""
    return bio.SequenceAnalysis(sequence)


# MikoshiLang Rules
# These integrate into the evaluator when mikoshibio is imported
# Only available if MikoshiLang is installed

if MIKOSHILANG_AVAILABLE:
    STRUCTURE_RULES = [
        # PDB Pack integration
        RuleDelayed(
            Expr("PackSearch", ["pdb", "query_"]),
            lambda query: pack_search_pdb(query)
        ),
        RuleDelayed(
            Expr("PackValue", ["pdb", "id_", "property_"]),
            lambda id, property: pack_value_pdb(id, property)
        ),
        
        # BioPython functions
        RuleDelayed(
            Expr("LoadPDB", ["pdb", "pdb_id_"]),
            lambda pdb_id: load_pdb_rule("pdb", pdb_id)
        ),
        RuleDelayed(
            Expr("LoadPDB", ["source_"]),
            lambda source: load_pdb_rule(source)
        ),
        RuleDelayed(
            Expr("GetSequence", ["structure_"]),
            lambda structure: get_sequence_rule(structure)
        ),
        RuleDelayed(
            Expr("GetSequence", ["structure_", "chain_id_"]),
            lambda structure, chain_id: get_sequence_rule(structure, chain_id)
        ),
        RuleDelayed(
            Expr("FindContacts", ["structure_", "distance_"]),
            lambda structure, distance: find_contacts_rule(structure, distance)
        ),
        RuleDelayed(
            Expr("CalculateRMSD", ["struct1_", "struct2_"]),
            lambda struct1, struct2: calculate_rmsd_rule(struct1, struct2)
        ),
        RuleDelayed(
            Expr("CalculateSecondaryStructure", ["structure_", "pdb_file_"]),
            lambda structure, pdb_file: secondary_structure_rule(structure, pdb_file)
        ),
        RuleDelayed(
            Expr("GetBindingSites", ["structure_", "ligand_"]),
            lambda structure, ligand: binding_sites_rule(structure, ligand)
        ),
        RuleDelayed(
            Expr("GetBindingSites", ["structure_", "ligand_", "distance_"]),
            lambda structure, ligand, distance: binding_sites_rule(structure, ligand, distance)
        ),
        RuleDelayed(
            Expr("SequenceAnalysis", ["sequence_"]),
            lambda sequence: sequence_analysis_rule(sequence)
        ),
    ]
else:
    STRUCTURE_RULES = []


__all__ = ["STRUCTURE_RULES", "MIKOSHILANG_AVAILABLE"]
