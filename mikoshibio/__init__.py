"""
MikoshiBio - Molecular Modeling Extension for MikoshiLang

Adds protein structure analysis, molecular dynamics, and docking capabilities.
"""

from .pdb_pack import PDBPack
from .biopython_bridge import (
    LoadPDB,
    GetSequence,
    FindContacts,
    CalculateRMSD,
    CalculateSecondaryStructure,
    GetBindingSites,
    SequenceAnalysis,
)

__version__ = "0.1.0"

__all__ = [
    # Knowledge pack
    "PDBPack",
    
    # BioPython functions
    "LoadPDB",
    "GetSequence",
    "FindContacts",
    "CalculateRMSD",
    "CalculateSecondaryStructure",
    "GetBindingSites",
    "SequenceAnalysis",
]
