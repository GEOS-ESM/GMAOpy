# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed
Some checks were added to semperpy/plot/mplib/layout.py to trap list objects where scalar objects were expected. This is likely the result of misinterpretation of matplotlib return values that are tuples or have become tuples. For example: val = plt.plot(a,b) should perhaps be val, = plt.plot(a,b). Other similar patches have been noted in the codes implemented by other developers. A better fix would be to correct the origin of the misassigned tuple values.

### Removed

### Deprecated

## 2025-04-10

### Fixed

- Removed passing major_locator to axis (this overwrites the defined labels)
- Passes tick values that correspond with tick labels and label range to axis  
- Commented out the redefining of ticks in axis  
