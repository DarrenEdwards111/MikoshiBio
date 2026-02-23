"""
Example: MD Trajectory Analysis + Molecular Docking Workflow

Demonstrates how to:
1. Analyze MD trajectories (RMSD, RMSF, contacts)
2. Perform molecular docking
3. Virtual screening

Note: Requires optional dependencies:
  pip install mikoshi-bio[all]
"""

import numpy as np
import matplotlib.pyplot as plt

# Check availability
try:
    from mikoshibio import (
        LoadTrajectory, TrajectoryInfo, CalculateTrajRMSD, 
        CalculateRMSF, CalculateRadius, AnalyzeTrajContacts
    )
    MD_AVAILABLE = True
except ImportError:
    MD_AVAILABLE = False
    print("⚠️  MDAnalysis not installed. MD features disabled.")
    print("    Install with: pip install mikoshi-bio[md]")

try:
    from mikoshibio import (
        DockLigand, CalculateBindingAffinity, CalculateBoxFromBindingSite,
        VirtualScreening
    )
    DOCKING_AVAILABLE = True
except ImportError:
    DOCKING_AVAILABLE = False
    print("⚠️  Vina not installed. Docking features disabled.")
    print("    Install with: pip install mikoshi-bio[docking]")


def example_md_analysis():
    """Example: Analyze MD trajectory."""
    if not MD_AVAILABLE:
        print("\nSkipping MD example (MDAnalysis not installed)")
        return
    
    print("\n" + "="*70)
    print("EXAMPLE 1: MD Trajectory Analysis")
    print("="*70)
    
    # Use MDAnalysis test data
    try:
        from MDAnalysis.tests.datafiles import PSF, DCD
    except ImportError:
        print("MDAnalysis test data not available")
        return
    
    print("\n[1] Loading trajectory...")
    universe = LoadTrajectory(PSF, DCD)
    info = TrajectoryInfo(universe)
    
    print(f"    Frames: {info['n_frames']}")
    print(f"    Atoms: {info['n_atoms']}")
    print(f"    Timestep: {info['timestep']:.2f} ps")
    print(f"    Total time: {info['total_time']:.2f} ps")
    
    print("\n[2] Calculating RMSD...")
    rmsd = CalculateTrajRMSD(universe, selection="backbone")
    print(f"    Mean RMSD: {np.mean(rmsd):.2f} Å")
    print(f"    Max RMSD: {np.max(rmsd):.2f} Å")
    print(f"    Std RMSD: {np.std(rmsd):.2f} Å")
    
    print("\n[3] Calculating RMSF...")
    rmsf = CalculateRMSF(universe, selection="backbone")
    print(f"    Mean RMSF: {np.mean(rmsf):.2f} Å")
    print(f"    Most flexible residue RMSF: {np.max(rmsf):.2f} Å")
    
    print("\n[4] Calculating radius of gyration...")
    rg = CalculateRadius(universe, selection="protein")
    print(f"    Mean Rg: {np.mean(rg):.2f} Å")
    print(f"    Rg range: {np.min(rg):.2f} - {np.max(rg):.2f} Å")
    
    # Plot results
    try:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # RMSD
        axes[0, 0].plot(rmsd)
        axes[0, 0].set_xlabel('Frame')
        axes[0, 0].set_ylabel('RMSD (Å)')
        axes[0, 0].set_title('Backbone RMSD')
        axes[0, 0].grid(True, alpha=0.3)
        
        # RMSF
        axes[0, 1].plot(rmsf)
        axes[0, 1].set_xlabel('Residue')
        axes[0, 1].set_ylabel('RMSF (Å)')
        axes[0, 1].set_title('Backbone RMSF')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Radius of gyration
        axes[1, 0].plot(rg)
        axes[1, 0].set_xlabel('Frame')
        axes[1, 0].set_ylabel('Rg (Å)')
        axes[1, 0].set_title('Radius of Gyration')
        axes[1, 0].grid(True, alpha=0.3)
        
        # RMSD distribution
        axes[1, 1].hist(rmsd, bins=30, alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('RMSD (Å)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('RMSD Distribution')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('md_analysis.png', dpi=150)
        print("\n✅ Saved plot: md_analysis.png")
        
    except Exception as e:
        print(f"\n⚠️  Could not generate plot: {e}")


def example_docking():
    """Example: Molecular docking."""
    if not DOCKING_AVAILABLE:
        print("\nSkipping docking example (Vina not installed)")
        return
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Molecular Docking")
    print("="*70)
    
    print("\nNote: This example shows the workflow structure.")
    print("For actual docking, you need:")
    print("  - receptor.pdbqt (prepared protein)")
    print("  - ligand.pdbqt (prepared ligand)")
    print("  - Docking box coordinates")
    
    print("\n[1] Typical docking workflow:")
    print("    a) Prepare receptor: ConvertPDBtoPDBQT('protein.pdb', is_receptor=True)")
    print("    b) Prepare ligand: ConvertPDBtoPDBQT('ligand.pdb', is_receptor=False)")
    print("    c) Define box: CalculateBoxFromBindingSite('protein.pdb', 'ATP')")
    print("    d) Dock: DockLigand('receptor.pdbqt', 'ligand.pdbqt', center, box_size)")
    
    print("\n[2] Virtual screening workflow:")
    print("    ligands = ['ligand1.pdbqt', 'ligand2.pdbqt', ...]")
    print("    results = VirtualScreening('receptor.pdbqt', ligands, center, box_size)")
    print("    top_hits = results[:10]  # Top 10 by affinity")


def example_integration():
    """Example: MD + Docking integration."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Integrated Workflow (MD + Docking)")
    print("="*70)
    
    print("\nUse case: Extract snapshots from MD and dock ligands")
    print("\nWorkflow:")
    print("  1. Run MD simulation → get trajectory")
    print("  2. Extract representative frames (e.g., most stable)")
    print("  3. Prepare each frame for docking")
    print("  4. Dock ligand to each snapshot")
    print("  5. Compare binding affinities across conformations")
    
    print("\nCode example:")
    print("""
    # Load trajectory
    universe = LoadTrajectory('md.psf', 'md.dcd')
    
    # Find most stable frame (lowest RMSD)
    rmsd = CalculateTrajRMSD(universe)
    stable_frame = np.argmin(rmsd)
    
    # Extract frame
    ExtractFrame(universe, stable_frame, 'snapshot.pdb')
    
    # Prepare for docking
    ConvertPDBtoPDBQT('snapshot.pdb', 'snapshot.pdbqt', is_receptor=True)
    
    # Dock ligand
    results = DockLigand('snapshot.pdbqt', 'ligand.pdbqt', 
                        center=(10, 10, 10), box_size=(20, 20, 20))
    
    print(f"Best affinity: {results[0]['affinity']} kcal/mol")
    """)


def example_autism_epigenetics_extension():
    """Example: How this extends the autism epigenetics meta-analysis."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Autism Epigenetics + MD/Docking")
    print("="*70)
    
    print("\nUse case: Study how methylation affects protein dynamics")
    print("\nWorkflow:")
    print("  1. Get protein structure for RELN, OXTR, MECP2, etc.")
    print("  2. Run MD simulations (normal vs methylated)")
    print("  3. Compare dynamics (RMSD, RMSF, Rg)")
    print("  4. Dock DNA to MECP2 (methyl-CpG binding)")
    print("  5. Compare binding affinity (unmethylated vs methylated DNA)")
    
    print("\nHypothesis testing:")
    print("  - Does MECP2 bind more tightly to methylated CpG?")
    print("  - Do RELN variants affect structural stability?")
    print("  - Does OXTR methylation change receptor flexibility?")
    
    print("\nIntegration with meta-analysis effect sizes:")
    print("  - Large effect sizes → expect big structural changes")
    print("  - Test if MD stability correlates with effect magnitude")
    print("  - Map epigenetic marks to flexible regions (high RMSF)")


def main():
    """Run all examples."""
    print("="*70)
    print("MikoshiBio Examples: MD Trajectory Analysis + Molecular Docking")
    print("="*70)
    
    # Check what's available
    print("\nInstalled features:")
    print(f"  BioPython: ✅ (always available)")
    print(f"  MDAnalysis: {'✅' if MD_AVAILABLE else '❌ (install with: pip install mikoshi-bio[md])'}")
    print(f"  Docking (Vina): {'✅' if DOCKING_AVAILABLE else '❌ (install with: pip install mikoshi-bio[docking])'}")
    
    # Run examples
    example_md_analysis()
    example_docking()
    example_integration()
    example_autism_epigenetics_extension()
    
    print("\n" + "="*70)
    print("Examples complete!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Install optional dependencies: pip install mikoshi-bio[all]")
    print("  2. Prepare your own structures/trajectories")
    print("  3. Run real MD simulations and docking")
    print("  4. Integrate with your meta-analysis data")


if __name__ == "__main__":
    main()
