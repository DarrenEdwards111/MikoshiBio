"""
Tests for PDB Knowledge Pack
"""

import pytest
from mikoshibio import PDBPack


def test_pdb_search():
    """Test PDB structure search."""
    pack = PDBPack()
    results = pack.search("crambin", limit=3)
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    if "error" not in results[0]:
        assert "id" in results[0]
        assert "label" in results[0]
        assert results[0]["source"] == "PDB"
        assert results[0]["license"] == "CC0 1.0"


def test_pdb_value_title():
    """Test getting structure title."""
    pack = PDBPack()
    result = pack.get_value("1CRN", "Title")
    
    if "error" not in result:
        assert "value" in result
        assert "crambin" in result["value"].lower() or "protein" in result["value"].lower()
        assert result["entity"] == "1CRN"
        assert result["license"] == "CC0 1.0"


def test_pdb_value_resolution():
    """Test getting structure resolution."""
    pack = PDBPack()
    result = pack.get_value("1CRN", "Resolution")
    
    if "error" not in result:
        assert "value" in result
        assert isinstance(result["value"], (int, float)) or result["value"] is None


def test_pdb_value_pdb_file():
    """Test getting PDB file URL."""
    pack = PDBPack()
    result = pack.get_value("1CRN", "PDBFile")
    
    assert "error" not in result
    assert "value" in result
    assert "https://files.rcsb.org/download/1CRN.pdb" in result["value"]


def test_pdb_value_method():
    """Test getting experimental method."""
    pack = PDBPack()
    result = pack.get_value("1CRN", "Method")
    
    if "error" not in result:
        assert "value" in result
        # Should be X-RAY DIFFRACTION or similar
        if result["value"]:
            assert isinstance(result["value"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
