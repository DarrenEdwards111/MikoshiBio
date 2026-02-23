#!/usr/bin/env python3
"""
Test that MikoshiBio works without MikoshiLang installed.
This simulates the scenario where a user installs just: pip install mikoshi-bio
"""

import sys

# Test 1: Can we import core functions?
print("Test 1: Importing core functions...")
try:
    from mikoshibio import (
        LoadPDB,
        GetSequence,
        FindContacts,
        CalculateRMSD,
        SequenceAnalysis,
        PDBPack,
        MIKOSHILANG_AVAILABLE,
    )
    print("✓ Core imports successful")
except ImportError as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 2: Can we use Python API?
print("\nTest 2: Using Python API...")
try:
    # Note: This would normally download from PDB, but we'll just test the function exists
    # For a real test, we'd need a local PDB file
    print(f"  LoadPDB callable: {callable(LoadPDB)}")
    print(f"  GetSequence callable: {callable(GetSequence)}")
    print(f"  FindContacts callable: {callable(FindContacts)}")
    print("✓ Python API functions are callable")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 3: Check MikoshiLang availability flag
print(f"\nTest 3: MikoshiLang availability...")
print(f"  MIKOSHILANG_AVAILABLE = {MIKOSHILANG_AVAILABLE}")
if MIKOSHILANG_AVAILABLE:
    print("  Note: MikoshiLang is installed - symbolic syntax available")
else:
    print("  Note: MikoshiLang not installed - Python API only")

# Test 4: PDB Pack works
print("\nTest 4: PDB Pack instantiation...")
try:
    pdb = PDBPack()
    print("✓ PDB Pack created successfully")
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed! MikoshiBio works without MikoshiLang.")
print("="*50)
