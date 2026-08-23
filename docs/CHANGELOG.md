# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html),
and this programmer does her best to follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)


## Unreleased

### Added

### Changed

### Removed

### Fixed

## [0.1.1]

### Added

- MIT License
- PyPi metadata

## [0.1.0]

### Added

- PerfLogger class as a direct functionnal copy of the PerformanceLogger class from my [boids project](https://github.com/ewigael/boids) (which now uses this package instead)

### Changed

- PerfLogger._instances is now a list to conserve creation order, added a classmethod ```get_all_instances``` to remove weak refs
