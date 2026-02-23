"""
MDAnalysis Integration for MikoshiLang
Molecular dynamics trajectory analysis tools.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np

try:
    import MDAnalysis as mda
    from MDAnalysis.analysis import rms, distances, align
    from MDAnalysis.analysis.rms import RMSD, RMSF
    from MDAnalysis.analysis.contacts import Contacts
    MDANALYSIS_AVAILABLE = True
except ImportError:
    MDANALYSIS_AVAILABLE = False


def LoadTrajectory(topology: str, trajectory: str, format: Optional[str] = None) -> Any:
    """
    Load MD trajectory for analysis.
    
    Args:
        topology: Topology file (PDB, PSF, etc.)
        trajectory: Trajectory file (DCD, XTC, TRR, etc.)
        format: Trajectory format (optional, auto-detected)
    
    Returns:
        MDAnalysis.Universe object
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed. Install with: pip install mikoshi-bio[md]")
    
    if format:
        universe = mda.Universe(topology, trajectory, format=format)
    else:
        universe = mda.Universe(topology, trajectory)
    
    return universe


def CalculateRMSD(universe: Any, selection: str = "backbone", reference: Optional[Any] = None) -> np.ndarray:
    """
    Calculate RMSD over trajectory.
    
    Args:
        universe: MDAnalysis Universe
        selection: Atom selection string (default: "backbone")
        reference: Reference frame (default: first frame)
    
    Returns:
        Array of RMSD values (Angstroms) for each frame
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    if reference is None:
        reference = universe
    
    R = RMSD(universe, reference, select=selection, groupselections=[selection])
    R.run()
    
    return R.rmsd[:, 2]  # RMSD values (column 2)


def CalculateRMSF(universe: Any, selection: str = "backbone") -> np.ndarray:
    """
    Calculate RMSF (root mean square fluctuation) for atoms.
    
    Args:
        universe: MDAnalysis Universe
        selection: Atom selection string
    
    Returns:
        Array of RMSF values per atom (Angstroms)
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    atoms = universe.select_atoms(selection)
    R = RMSF(atoms).run()
    
    return R.rmsf


def CalculateRadius(universe: Any, selection: str = "protein") -> np.ndarray:
    """
    Calculate radius of gyration over trajectory.
    
    Args:
        universe: MDAnalysis Universe
        selection: Atom selection string
    
    Returns:
        Array of Rg values (Angstroms) for each frame
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    protein = universe.select_atoms(selection)
    rg_values = []
    
    for ts in universe.trajectory:
        rg_values.append(protein.radius_of_gyration())
    
    return np.array(rg_values)


def AnalyzeContacts(universe: Any, selection1: str, selection2: str, 
                    distance: float = 4.5) -> Dict[str, Any]:
    """
    Analyze contacts between two selections over trajectory.
    
    Args:
        universe: MDAnalysis Universe
        selection1: First selection (e.g., "protein")
        selection2: Second selection (e.g., "resname ATP")
        distance: Contact distance threshold (Angstroms)
    
    Returns:
        Dict with contact timeseries and statistics
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    sel1 = universe.select_atoms(selection1)
    sel2 = universe.select_atoms(selection2)
    
    contacts = Contacts(universe, select=(selection1, selection2), 
                       refgroup=(sel1, sel2), radius=distance)
    contacts.run()
    
    return {
        "timeseries": contacts.timeseries.tolist(),
        "mean_contacts": float(np.mean(contacts.timeseries[:, 1])),
        "std_contacts": float(np.std(contacts.timeseries[:, 1])),
        "max_contacts": int(np.max(contacts.timeseries[:, 1])),
        "min_contacts": int(np.min(contacts.timeseries[:, 1])),
    }


def AlignTrajectory(universe: Any, reference: Any, selection: str = "backbone") -> None:
    """
    Align trajectory to reference structure.
    
    Args:
        universe: MDAnalysis Universe (modified in-place)
        reference: Reference structure
        selection: Atom selection for alignment
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    align.AlignTraj(universe, reference, select=selection, in_memory=False).run()


def ExtractFrame(universe: Any, frame: int, output_path: str) -> None:
    """
    Extract a single frame and save as PDB.
    
    Args:
        universe: MDAnalysis Universe
        frame: Frame number to extract
        output_path: Output PDB file path
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    universe.trajectory[frame]
    
    with mda.Writer(output_path, multiframe=False) as W:
        W.write(universe.atoms)


def CalculateDistances(universe: Any, selection1: str, selection2: str) -> np.ndarray:
    """
    Calculate distances between two atom selections over trajectory.
    
    Args:
        universe: MDAnalysis Universe
        selection1: First atom selection
        selection2: Second atom selection
    
    Returns:
        Array of distances (Angstroms) for each frame
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    sel1 = universe.select_atoms(selection1)
    sel2 = universe.select_atoms(selection2)
    
    dist_values = []
    for ts in universe.trajectory:
        d = distances.dist(sel1, sel2)
        dist_values.append(d[2][0])  # Distance value
    
    return np.array(dist_values)


def TrajectoryInfo(universe: Any) -> Dict[str, Any]:
    """
    Get trajectory metadata.
    
    Returns:
        Dict with frames, timestep, duration, atoms count
    """
    if not MDANALYSIS_AVAILABLE:
        raise ImportError("MDAnalysis not installed")
    
    return {
        "n_frames": len(universe.trajectory),
        "n_atoms": len(universe.atoms),
        "timestep": universe.trajectory.dt,  # ps
        "total_time": universe.trajectory.totaltime,  # ps
        "has_velocities": universe.trajectory.has_velocities,
        "has_forces": universe.trajectory.has_forces,
    }


# Export all functions
__all__ = [
    "LoadTrajectory",
    "CalculateRMSD",
    "CalculateRMSF",
    "CalculateRadius",
    "AnalyzeContacts",
    "AlignTrajectory",
    "ExtractFrame",
    "CalculateDistances",
    "TrajectoryInfo",
]
