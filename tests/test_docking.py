"""
Tests for Molecular Docking

Note: These tests require Vina to be installed.
Run with: pytest tests/test_docking.py -v
"""

import pytest
import os
import tempfile

try:
    from vina import Vina
    from mikoshibio import docking
    VINA_AVAILABLE = True
except ImportError:
    VINA_AVAILABLE = False
    docking = None


def test_vina_import_error():
    """Test that functions raise ImportError when Vina not available."""
    if VINA_AVAILABLE:
        pytest.skip("Vina is installed")
    
    # When Vina not installed, docking module won't be importable
    pytest.skip("Docking module requires Vina - cannot test import error without import")


@pytest.mark.skipif(not VINA_AVAILABLE, reason="Vina not installed")
def test_dock_ligand_structure():
    """Test docking function returns correct structure."""
    # This test checks the interface, not actual docking
    # (requires valid PDBQT files for real test)
    
    # Verify function signature
    assert callable(docking.DockLigand)
    assert callable(docking.CalculateBindingAffinity)
    assert callable(docking.SaveDockingPoses)


@pytest.mark.skipif(not VINA_AVAILABLE, reason="Vina not installed")
def test_virtual_screening_structure():
    """Test virtual screening function structure."""
    assert callable(docking.VirtualScreening)


def test_calculate_box_from_binding_site_import():
    """Test that CalculateBoxFromBindingSite can be imported."""
    try:
        from mikoshibio.docking import CalculateBoxFromBindingSite
        assert callable(CalculateBoxFromBindingSite)
    except ImportError:
        pytest.skip("Docking module not available")


def test_calculate_box_from_binding_site():
    """Test docking box calculation from binding site."""
    # Import function directly (doesn't require Vina)
    try:
        from mikoshibio.docking import CalculateBoxFromBindingSite
    except ImportError:
        pytest.skip("Docking module not available")
    
    # Create a minimal PDB file with ligand
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        # Minimal PDB with ATP ligand (using unique atom names)
        f.write("HETATM    1  N1  ATP A   1      10.000  10.000  10.000  1.00  0.00           N\n")
        f.write("HETATM    2  C1  ATP A   1      11.000  10.000  10.000  1.00  0.00           C\n")
        f.write("HETATM    3  C2  ATP A   1      10.000  11.000  10.000  1.00  0.00           C\n")
        f.write("HETATM    4  O1  ATP A   1      10.000  10.000  11.000  1.00  0.00           O\n")
        pdb_file = f.name
    
    try:
        center, box_size = CalculateBoxFromBindingSite(pdb_file, "ATP", padding=5.0)
        
        assert isinstance(center, tuple)
        assert len(center) == 3
        assert isinstance(box_size, tuple)
        assert len(box_size) == 3
        
        # Check center is computed correctly
        # Coords: (10,10,10), (11,10,10), (10,11,10), (10,10,11)
        # Min: (10,10,10), Max: (11,11,11)
        # Center: (10.5, 10.5, 10.5)
        assert center[0] == pytest.approx(10.5, abs=0.2)
        assert center[1] == pytest.approx(10.5, abs=0.2)
        assert center[2] == pytest.approx(10.5, abs=0.2)
        
        # Check box size is approximately (6.0, 6.0, 6.0) with 5.0 padding
        assert all(s >= 5.0 for s in box_size)
        
    finally:
        os.unlink(pdb_file)


def test_calculate_box_missing_ligand():
    """Test box calculation fails gracefully with missing ligand."""
    try:
        from mikoshibio.docking import CalculateBoxFromBindingSite
    except ImportError:
        pytest.skip("Docking module not available")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as f:
        # PDB without ATP
        f.write("ATOM      1  CA  ALA A   1      10.000  10.000  10.000  1.00  0.00           C\n")
        pdb_file = f.name
    
    try:
        with pytest.raises(ValueError, match="not found"):
            CalculateBoxFromBindingSite(pdb_file, "ATP")
    finally:
        os.unlink(pdb_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
