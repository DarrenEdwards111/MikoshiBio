"""
MikoshiBio - Molecular Modeling Extension

Provides Python API for protein structure analysis, molecular dynamics, and docking.
Optional MikoshiLang integration for symbolic/Wolfram-style syntax.

Install modes:
  pip install mikoshi-bio              # Python API only
  pip install mikoshi-bio[symbolic]    # + MikoshiLang integration
  pip install mikoshi-bio[md]          # + MDAnalysis
  pip install mikoshi-bio[docking]     # + AutoDock Vina
  pip install mikoshi-bio[all]         # All features
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

# Check for optional MikoshiLang integration
try:
    from .structure_rules import STRUCTURE_RULES, MIKOSHILANG_AVAILABLE
except ImportError:
    MIKOSHILANG_AVAILABLE = False
    STRUCTURE_RULES = []

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

__version__ = "0.2.1"

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
    
    # Feature flags
    "MIKOSHILANG_AVAILABLE",
    "MDANALYSIS_AVAILABLE",
    "VINA_AVAILABLE",
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

