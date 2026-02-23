# MikoshiBio

**Molecular Modeling Extension for MikoshiLang**

Adds protein structure analysis, molecular dynamics trajectory analysis, and molecular docking capabilities to MikoshiLang.

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

### Planned Features
- MDAnalysis trajectory analysis
- AutoDock Vina molecular docking
- Py3Dmol/NGLView visualization
- RDKit molecular descriptors

## Installation

```bash
# Basic installation
pip install mikoshi-bio

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

### Query PDB Database

```python
from mikoshilang import parse_and_eval
import mikoshibio  # Loads PDB pack + structure functions

# Search for structures
parse_and_eval('PackSearch["pdb", "hemoglobin"]')
# → [{"id": "1A3N", "label": "Crystal Structure of Human Hemoglobin", ...}]

# Get structure metadata
parse_and_eval('PackValue["pdb", "1CRN", "Resolution"]')
# → {"value": 1.5, "entity": "1CRN", ...}

# Download structure
parse_and_eval('PackValue["pdb", "1CRN", "PDBFile"]')
# → {"value": "https://files.rcsb.org/download/1CRN.pdb", ...}
```

### Load and Analyze Structures

```python
from mikoshilang import Expr
from mikoshibio import LoadPDB, GetSequence, FindContacts, CalculateRMSD

# Load structure from PDB
structure = LoadPDB("pdb", "1CRN")

# Extract sequence
seq = GetSequence(structure)
print(f"Sequence: {seq}")

# Find contacts within 5 Angstroms
contacts = FindContacts(structure, distance=5.0)
print(f"Found {len(contacts)} contacts")

# Analyze sequence properties
from mikoshibio import SequenceAnalysis
props = SequenceAnalysis(seq)
print(f"MW: {props['molecular_weight']:.2f} Da")
print(f"pI: {props['isoelectric_point']:.2f}")
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

## Usage with MikoshiLang Syntax

MikoshiBio integrates seamlessly with MikoshiLang's Wolfram-style syntax:

```python
from mikoshilang import parse_and_eval
import mikoshibio

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
