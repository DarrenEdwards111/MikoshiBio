"""
Example: Autism Epigenetics Genes + Protein Structure Analysis

Demonstrates how MikoshiBio can augment a meta-analysis by adding
structural biology context to epigenetic findings.
"""

from mikoshilang import parse_and_eval
import mikoshibio
from mikoshibio import LoadPDB, GetSequence, SequenceAnalysis, FindContacts
import pandas as pd


# Genes from Track A meta-analysis (significant findings)
GENES = {
    "RELN": "Reelin - neurodevelopmental, synaptic plasticity",
    "OXTR": "Oxytocin receptor - social behavior, bonding",
    "MECP2": "Methyl-CpG binding protein 2 - gene regulation",
    "UBE3A": "Ubiquitin E3 ligase - Angelman syndrome",
    "GABRB3": "GABA receptor subunit - inhibitory neurotransmission",
}


def analyze_gene_protein(gene_symbol, description):
    """Query structural data for a gene and analyze protein properties."""
    
    print(f"\n{'='*70}")
    print(f"Gene: {gene_symbol}")
    print(f"Function: {description}")
    print('='*70)
    
    # 1. Search AlphaFold for predicted structure
    print("\n[1] Querying AlphaFold database...")
    af_results = parse_and_eval(f'PackSearch["alphafold", "{gene_symbol}"]')
    
    if af_results and len(af_results) > 0 and "error" not in af_results[0]:
        uniprot_id = af_results[0]["id"]
        print(f"    Found AlphaFold prediction: {uniprot_id}")
        print(f"    Label: {af_results[0]['label']}")
        
        # Get confidence score
        confidence = parse_and_eval(f'PackValue["alphafold", "{uniprot_id}", "Confidence"]')
        if "error" not in confidence:
            print(f"    pLDDT confidence: {confidence['value']}")
    else:
        print("    No AlphaFold prediction found")
        uniprot_id = None
    
    # 2. Search PDB for experimental structures
    print("\n[2] Querying PDB for experimental structures...")
    pdb_results = parse_and_eval(f'PackSearch["pdb", "{gene_symbol}"]')
    
    if pdb_results and len(pdb_results) > 0 and "error" not in pdb_results[0]:
        pdb_id = pdb_results[0]["id"]
        print(f"    Found experimental structure: {pdb_id}")
        print(f"    Title: {pdb_results[0]['label']}")
        
        # Get structure metadata
        resolution = parse_and_eval(f'PackValue["pdb", "{pdb_id}", "Resolution"]')
        method = parse_and_eval(f'PackValue["pdb", "{pdb_id}", "Method"]')
        
        if "error" not in resolution:
            print(f"    Resolution: {resolution['value']} Å")
        if "error" not in method:
            print(f"    Method: {method['value']}")
        
        # 3. Load structure and analyze
        print("\n[3] Loading structure for analysis...")
        try:
            structure = LoadPDB("pdb", pdb_id)
            
            # Extract sequence
            sequence = GetSequence(structure)
            print(f"    Sequence length: {len(sequence)} residues")
            print(f"    First 50 residues: {sequence[:50]}...")
            
            # Analyze sequence properties
            print("\n[4] Analyzing protein properties...")
            props = SequenceAnalysis(sequence)
            
            print(f"    Molecular weight: {props['molecular_weight']:.2f} Da")
            print(f"    Isoelectric point: {props['isoelectric_point']:.2f}")
            print(f"    Instability index: {props['instability_index']:.2f}")
            print(f"    Aromaticity: {props['aromaticity']:.4f}")
            
            # Secondary structure fraction
            ss = props['secondary_structure_fraction']
            print(f"    Secondary structure: {ss[0]:.1%} helix, {ss[1]:.1%} turn, {ss[2]:.1%} sheet")
            
            # 5. Find structural contacts (potential interaction sites)
            print("\n[5] Finding inter-atomic contacts...")
            contacts = FindContacts(structure, distance=4.0)
            print(f"    Found {len(contacts)} contacts within 4.0 Å")
            
            if contacts:
                # Show first few
                print("    Sample contacts:")
                for c in contacts[:5]:
                    print(f"      {c['atom1']} <-> {c['atom2']} ({c['distance']:.2f} Å)")
            
            return {
                "gene": gene_symbol,
                "pdb_id": pdb_id,
                "uniprot_id": uniprot_id,
                "sequence_length": len(sequence),
                "molecular_weight": props['molecular_weight'],
                "pI": props['isoelectric_point'],
                "resolution": resolution.get("value"),
                "method": method.get("value"),
            }
            
        except Exception as e:
            print(f"    Error loading structure: {e}")
            return None
    else:
        print("    No experimental structure found in PDB")
        return None


def main():
    """Analyze all epigenetic genes from meta-analysis."""
    
    print("="*70)
    print("Autism Epigenetics Meta-Analysis: Protein Structure Context")
    print("="*70)
    print("\nAnalyzing significant genes from Track A (k≥2, p<0.05)\n")
    
    results = []
    
    for gene, desc in GENES.items():
        result = analyze_gene_protein(gene, desc)
        if result:
            results.append(result)
    
    # Summary table
    if results:
        print("\n" + "="*70)
        print("SUMMARY TABLE")
        print("="*70 + "\n")
        
        df = pd.DataFrame(results)
        print(df.to_string(index=False))
        
        # Save to CSV
        df.to_csv("autism_epigenetics_protein_summary.csv", index=False)
        print("\nSaved to: autism_epigenetics_protein_summary.csv")
    
    # Future: Correlation analysis
    print("\n" + "="*70)
    print("FUTURE ANALYSIS IDEAS:")
    print("="*70)
    print("1. Correlate protein MW with effect size magnitude")
    print("2. Check if DNA-binding proteins show stronger methylation effects")
    print("3. Analyze binding site conservation across species")
    print("4. Map epigenetic marks to 3D structure (PTM sites)")
    print("5. Predict structural impact of autism-associated variants")


if __name__ == "__main__":
    main()
