# Changelog

All notable changes to MikoshiBio will be documented in this file.

## [0.2.1] - 2026-02-23

### Changed
- **MikoshiLang is now optional** - core functionality works without it
  - Install with `pip install mikoshi-bio` for Python API only
  - Install with `pip install mikoshi-bio[symbolic]` for MikoshiLang integration
- Updated README to show both Python and symbolic usage modes
- Added `MIKOSHILANG_AVAILABLE` flag for runtime feature detection
- Graceful degradation when MikoshiLang is not installed

### Why This Change?
BioPython users who just want Python wrappers don't need the symbolic computation engine.
This keeps the base install lightweight while preserving advanced features for those who want them.

## [0.2.0] - 2026-02-22

### Added
- MDAnalysis integration for trajectory analysis
  - LoadTrajectory, CalculateRMSD, CalculateRMSF, CalculateRadius
  - AnalyzeContacts, AlignTrajectory, ExtractFrame, CalculateDistances, TrajectoryInfo
- AutoDock Vina integration (planned)
- 9 new trajectory analysis functions

### Fixed
- PDB search API: changed from `"service": "text"` to `"service": "full_text"`

## [0.1.0] - 2026-02-21

### Added
- Initial release
- PDB knowledge pack (8th domain pack)
- BioPython integration
  - LoadPDB, GetSequence, FindContacts, CalculateRMSD
  - CalculateSecondaryStructure, GetBindingSites, SequenceAnalysis
- MikoshiLang structure rules for Wolfram-style syntax
- Real-world example: autism epigenetics meta-analysis augmentation
