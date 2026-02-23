# MikoshiBio

<p align="center">
  <img src="mikoshibio-logo.jpg" alt="MikoshiBio" width="400">
</p>

[![PyPI](https://img.shields.io/pypi/v/mikoshi-bio)](https://pypi.org/project/mikoshi-bio/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-8%20passed-brightgreen)]()

**Molecular Modeling for Python & MikoshiLang**

Protein structure analysis, molecular dynamics, and docking tools.
Use as a pure Python library or with MikoshiLang's symbolic/Wolfram-style syntax.

## Features

### 8th Knowledge Pack: PDB (Protein Data Bank)
- Query 200,000+ experimental protein structures
- Get resolution, experimental method, release dates
- Download PDB/mmCIF files
- Extract sequences from structures

### BioPython Integration
- Load PDB structures from files, URLs, or PDB IDs
- Calculate RMSD between structures
- Find inter-atomic contacts
- Identify binding sites
- Secondary structure analysis (DSSP)
- Sequence property analysis

### MDAnalysis Integration (v0.2.0) ✨ NEW
- Load and analyze MD trajectories
- Calculate RMSD, RMSF, radius of gyration
- Track contacts and distances over time
- Extract frames and align trajectories
- Support for DCD, XTC, TRR formats

### Molecular Docking (v0.2.0) ✨ NEW
- AutoDock Vina integration
- Protein-ligand docking
- Binding affinity calculation
- Virtual screening
- Automatic docking box calculation
- PDB to PDBQT conversion

### Planned Features
- Py3Dmol/NGLView visualization (v0.3.0)
- RDKit molecular descriptors (v0.4.0)
- Advanced trajectory analysis (v0.5.0)

## Installation

```bash
# Python API only (BioPython + NumPy)
pip install mikoshi-bio

# With MikoshiLang symbolic/Wolfram-style syntax
pip install mikoshi-bio[symbolic]

# With molecular dynamics support
pip install mikoshi-bio[md]

# With docking tools
pip install mikoshi-bio[docking]

# With visualization
pip install mikoshi-bio[visualization]

# Everything
pip install mikoshi-bio[all]
```

## Quick Start

### Python API (No MikoshiLang Required)

```python
from mikoshibio import LoadPDB, GetSequence, FindContacts, SequenceAnalysis

# Load structure from PDB
structure = LoadPDB("pdb", "1CRN")

# Extract sequence
seq = GetSequence(structure)
print(f"Sequence: {seq}")

# Find contacts within 5 Angstroms
contacts = FindContacts(structure, distance=5.0)
print(f"Found {len(contacts)} contacts")

# Analyze sequence properties
props = SequenceAnalysis(seq)
print(f"MW: {props['molecular_weight']:.2f} Da")
print(f"pI: {props['isoelectric_point']:.2f}")
```

### Query PDB Database

```python
from mikoshibio import PDBPack

pdb = PDBPack()

# Search for structures
results = pdb.search("hemoglobin", limit=5)
# → [{"id": "1A3N", "label": "Crystal Structure of Human Hemoglobin", ...}]

# Get structure metadata
resolution = pdb.get_value("1CRN", "Resolution")
print(f"Resolution: {resolution['value']} Å")

# Get PDB file URL
pdb_url = pdb.get_value("1CRN", "PDBFile")
# → "https://files.rcsb.org/download/1CRN.pdb"
```

### Compare Structures

```python
# Load two structures
ref = LoadPDB("pdb", "1CRN")
mobile = LoadPDB("pdb", "2CRN")

# Calculate RMSD
rmsd = CalculateRMSD(ref, mobile)
print(f"RMSD: {rmsd:.2f} Å")
```

### Find Binding Sites

```python
# Load structure with ligand
structure = LoadPDB("pdb", "1ATP")

# Find residues near ATP
binding_residues = GetBindingSites(structure, "ATP", distance=4.0)
print(f"Binding site residues: {binding_residues}")
```

## Optional: MikoshiLang Symbolic Syntax

Install with `pip install mikoshi-bio[symbolic]` for Wolfram-style symbolic computation:

```python
from mikoshilang import parse_and_eval
import mikoshibio  # Registers structure rules

# Check if symbolic features are available
from mikoshibio import MIKOSHILANG_AVAILABLE
if not MIKOSHILANG_AVAILABLE:
    print("Install mikoshi-bio[symbolic] for MikoshiLang integration")

# Load structure
result = parse_and_eval('LoadPDB["pdb", "1CRN"]')

# Get sequence (stored in variable)
parse_and_eval('seq = GetSequence[result]')

# Analyze sequence
parse_and_eval('SequenceAnalysis[seq]')

# Find contacts
parse_and_eval('FindContacts[result, 5.0]')
```

## Integration with Meta-Analysis Workflow

**Example: Autism Epigenetics + Protein Structure**

```python
from mikoshilang import parse_and_eval
import mikoshibio

# For each epigenetic gene in your meta-analysis
genes = ["RELN", "OXTR", "MECP2", "UBE3A"]

for gene in genes:
    # Query AlphaFold for predicted structure
    alphafold = parse_and_eval(f'PackSearch["alphafold", "{gene}"]')
    
    # Query PDB for experimental structures
    pdb = parse_and_eval(f'PackSearch["pdb", "{gene}"]')
    
    # Get sequence from best structure
    if pdb and len(pdb) > 0:
        structure = LoadPDB("pdb", pdb[0]["id"])
        sequence = GetSequence(structure)
        
        # Analyze protein properties
        props = SequenceAnalysis(sequence)
        print(f"{gene}: MW={props['molecular_weight']:.0f} Da, pI={props['isoelectric_point']:.2f}")
        
        # Check for DNA-binding domains (future feature)
        # binding_sites = GetBindingSites(structure, "DNA", distance=4.0)
```

## Architecture

```
mikoshibio/
├── pdb_pack.py           # PDB knowledge pack (8th pack)
├── biopython_bridge.py   # BioPython wrappers
├── structure_rules.py    # MikoshiLang evaluator rules
├── mdanalysis_tools.py   # MD trajectory analysis (planned)
├── docking.py            # AutoDock Vina interface (planned)
└── visualization.py      # Molecular viewers (planned)
```

## Knowledge Packs Comparison

| Pack | Domain | Coverage | License |
|------|--------|----------|---------|
| PubChem | Small molecules | 100M+ | Public Domain |
| AlphaFold | Predicted structures | 200M+ | CC BY 4.0 |
| **PDB** | Experimental structures | 200K+ | CC0 1.0 |

## Requirements

**Core:**
- Python ≥ 3.9
- mikoshilang ≥ 3.5.0
- biopython ≥ 1.80

**Optional:**
- MDAnalysis ≥ 2.0 (trajectory analysis)
- AutoDock Vina ≥ 1.2 (molecular docking)
- py3Dmol ≥ 2.0 (visualization)
- RDKit ≥ 2022.9 (molecular descriptors)

## Functions Reference

### Knowledge Pack Functions

```python
PackSearch["pdb", query, limit=5]         # Search PDB structures
PackValue["pdb", pdb_id, property]        # Get structure metadata
```

**Properties:** Title, Method, Resolution, ReleaseDate, Organism, Chains, Sequence, PDBFile, MMCIF

### Structure Analysis Functions

```python
LoadPDB["pdb", pdb_id]                    # Load from PDB
LoadPDB[file_path]                        # Load from file
GetSequence[structure]                    # Extract amino acid sequence
FindContacts[structure, distance]         # Find inter-atomic contacts
CalculateRMSD[struct1, struct2]           # Structural alignment
CalculateSecondaryStructure[struct, file] # DSSP analysis
GetBindingSites[structure, ligand]        # Binding site residues
SequenceAnalysis[sequence]                # Protein properties
```

## Development Status

- ✅ **v0.1.0:** PDB pack + BioPython integration
- ⏳ **v0.2.0:** MDAnalysis trajectory tools
- ⏳ **v0.3.0:** AutoDock Vina docking interface
- ⏳ **v0.4.0:** Molecular visualization (Py3Dmol/NGLView)
- ⏳ **v0.5.0:** RDKit molecular descriptors

## License

Apache 2.0

## Links

- **GitHub:** https://github.com/DarrenEdwards111/MikoshiBio
- **MikoshiLang:** https://pypi.org/project/mikoshilang/
- **Documentation:** https://mikoshi.co.uk/mikoshilang

## Citation

If you use MikoshiBio in your research, please cite:

```bibtex
@software{mikoshibio2026,
  title = {MikoshiBio: Molecular Modeling Extension for MikoshiLang},
  author = {Mikoshi Ltd},
  year = {2026},
  url = {https://github.com/DarrenEdwards111/MikoshiBio}
}
```

Built by **Mikoshi Ltd** as an extension to MikoshiLang.
