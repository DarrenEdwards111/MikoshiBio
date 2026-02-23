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

# MDAnalysis tools (optional - requires mdanalysis)
try:
    from .mdanalysis_tools import (
        LoadTrajectory,
        CalculateRMSD as CalculateTrajRMSD,
        CalculateRMSF,
        CalculateRadius,
        AnalyzeContacts as AnalyzeTrajContacts,
        AlignTrajectory,
        ExtractFrame,
        CalculateDistances,
        TrajectoryInfo,
    )
    MDANALYSIS_AVAILABLE = True
except ImportError:
    MDANALYSIS_AVAILABLE = False

# Docking tools (optional - requires vina)
try:
    from .docking import (
        DockLigand,
        CalculateBindingAffinity,
        SaveDockingPoses,
        ConvertPDBtoPDBQT,
        CalculateBoxFromBindingSite,
        VirtualScreening,
    )
    VINA_AVAILABLE = True
except ImportError:
    VINA_AVAILABLE = False

__version__ = "0.2.0"

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

# Add MD functions if available
if MDANALYSIS_AVAILABLE:
    __all__.extend([
        "LoadTrajectory",
        "CalculateTrajRMSD",
        "CalculateRMSF",
        "CalculateRadius",
        "AnalyzeTrajContacts",
        "AlignTrajectory",
        "ExtractFrame",
        "CalculateDistances",
        "TrajectoryInfo",
    ])

# Add docking functions if available
if VINA_AVAILABLE:
    __all__.extend([
        "DockLigand",
        "CalculateBindingAffinity",
        "SaveDockingPoses",
        "ConvertPDBtoPDBQT",
        "CalculateBoxFromBindingSite",
        "VirtualScreening",
    ])

