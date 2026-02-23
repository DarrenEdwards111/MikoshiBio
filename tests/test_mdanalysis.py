"""
Tests for MDAnalysis Integration

Note: These tests require MDAnalysis to be installed.
Run with: pytest tests/test_mdanalysis.py -v
"""

import pytest
import numpy as np

try:
    import MDAnalysis as mda
    from mikoshibio import mdanalysis_tools
    MDANALYSIS_AVAILABLE = True
except ImportError:
    MDANALYSIS_AVAILABLE = False
    mdanalysis_tools = None


@pytest.mark.skipif(not MDANALYSIS_AVAILABLE, reason="MDAnalysis not installed")
def test_load_trajectory():
    """Test trajectory loading (using MDAnalysis test data)."""
    from MDAnalysis.tests.datafiles import PSF, DCD
    
    universe = mdanalysis_tools.LoadTrajectory(PSF, DCD)
    
    assert universe is not None
    assert len(universe.atoms) > 0
    assert len(universe.trajectory) > 0


@pytest.mark.skipif(not MDANALYSIS_AVAILABLE, reason="MDAnalysis not installed")
def test_trajectory_info():
    """Test trajectory metadata extraction."""
    from MDAnalysis.tests.datafiles import PSF, DCD
    
    universe = mdanalysis_tools.LoadTrajectory(PSF, DCD)
    info = mdanalysis_tools.TrajectoryInfo(universe)
    
    assert "n_frames" in info
    assert "n_atoms" in info
    assert "timestep" in info
    assert info["n_frames"] > 0
    assert info["n_atoms"] > 0


@pytest.mark.skipif(not MDANALYSIS_AVAILABLE, reason="MDAnalysis not installed")
def test_calculate_rmsd():
    """Test RMSD calculation."""
    from MDAnalysis.tests.datafiles import PSF, DCD
    
    universe = mdanalysis_tools.LoadTrajectory(PSF, DCD)
    rmsd = mdanalysis_tools.CalculateRMSD(universe, selection="backbone")
    
    assert isinstance(rmsd, np.ndarray)
    assert len(rmsd) == len(universe.trajectory)
    assert rmsd[0] == pytest.approx(0.0, abs=0.1)  # First frame RMSD ~ 0


@pytest.mark.skipif(not MDANALYSIS_AVAILABLE, reason="MDAnalysis not installed")
def test_calculate_rmsf():
    """Test RMSF calculation."""
    from MDAnalysis.tests.datafiles import PSF, DCD
    
    universe = mdanalysis_tools.LoadTrajectory(PSF, DCD)
    rmsf = mdanalysis_tools.CalculateRMSF(universe, selection="backbone")
    
    assert isinstance(rmsf, np.ndarray)
    assert len(rmsf) > 0
    assert np.all(rmsf >= 0)  # RMSF should be non-negative


@pytest.mark.skipif(not MDANALYSIS_AVAILABLE, reason="MDAnalysis not installed")
def test_calculate_radius():
    """Test radius of gyration calculation."""
    from MDAnalysis.tests.datafiles import PSF, DCD
    
    universe = mdanalysis_tools.LoadTrajectory(PSF, DCD)
    rg = mdanalysis_tools.CalculateRadius(universe, selection="protein")
    
    assert isinstance(rg, np.ndarray)
    assert len(rg) == len(universe.trajectory)
    assert np.all(rg > 0)  # Rg should be positive


def test_mdanalysis_import_error():
    """Test that functions raise ImportError when MDAnalysis not available."""
    if MDANALYSIS_AVAILABLE:
        pytest.skip("MDAnalysis is installed")
    
    # When MD Analysis not installed, module won't be importable
    pytest.skip("MDAnalysis module requires MDAnalysis - cannot test import error without import")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
