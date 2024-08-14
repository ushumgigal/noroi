# Change Log {#ChangeLog}
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.1.1] - 2024-08-14

### Fixed

- Handling ommited setup dictionary keys (optional ones.)
- Default config vals for HexMaster & setup dictionary for HexMaster is now optional

## [1.1.0] - 2024-08-13

### Fixed

- More forgiving aligners
- No cell is painted on overflow or underflow anymore

### Added

- Screen resize is now a func, also optionally performed on HexMaster start
- Relative Div/inner sizes and margins

## [1.0.1] - 2024-08-11

### Fixed

- Terminal size is checked and expanded if too small before Div's visual update.

## [1.0.0] - 2024-08-10
  
### Added
 
- noroi package
- core module with classes:
  - Attribute
  - Key
  - DivStatus
  - Alignment
  - AnchorEdges
  - DivTypes
  - ColorHandler
  - Div
  - Label
  - Button
  - TextArea
- wrapper module with class:
  - HexMaster
