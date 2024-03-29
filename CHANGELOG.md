# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0 - Unreleased]

- WIP

## [0.7.0]

### Added
- support for python 3.10
- black in pre-commit
- isort in pre-commit
- dependency `httpx`
- display required time in console

### Changed
- moved from synchronous to asynchronous http calls for the PyPiJSON API

### Removed
- support for python 3.6 and pypy3 <= 3.6
- pylama from pre-commit
- dependency `requests`
- dependency `pyopenssl`

## [0.6.0]

### Changed
- add support for python 3.9
- drop support for python 3.5

## [0.5.0]

### Changed
- drop support for python 2.7, 3.4 and pypy2

## [0.4.2]

### Changed
- add license information to console output

## [0.4.1]

### Changed
- add default values for `categorized_package_data` to avoid crash on packages not available on pypi

## [0.4.0]

### Added
- `-pr`, `--pre-releases` parameter to explicitly enable display of pre-releases in console

### Changed
- Module structure for module and console functions

## [0.3.1]
### Changed
- Replace PyPi URL with new PyPi Warehouse URL

## [0.3.0]
### Changed
- Replace pip internal functions. Since the release of pip 9.0.2 the import of pip related libraries is not allowed anymore pypa/pip#5081

## [0.2.0]
### Added
- Adds license information
- Information about pre-release versions

## [0.1.5]
### Changed
- Fixes docs on pypi

## [0.1.4]
### Changed
- Several fixes

## [0.1.3]
### Changed
- Several fixes

## [0.1.2]
### Changed
- Several fixes

## [0.1.1]
### Changed
- Several fixes

## [0.1.0]
### Added
- Initial Release

[0.8.0 - Unreleased]: https://github.com/nezhar/updatable
[0.7.0]: https://pypi.org/project/updatable/0.7.0/
[0.6.0]: https://pypi.org/project/updatable/0.6.0/
[0.5.0]: https://pypi.org/project/updatable/0.5.0/
[0.4.2]: https://pypi.org/project/updatable/0.4.2/
[0.4.1]: https://pypi.org/project/updatable/0.4.1/
[0.4.0]: https://pypi.org/project/updatable/0.4.0/
[0.3.1]: https://pypi.org/project/updatable/0.3.1/
[0.3.0]: https://pypi.org/project/updatable/0.3.0/
[0.2.0]: https://pypi.org/project/updatable/0.2.0/
[0.1.5]: https://pypi.org/project/updatable/0.1.5/
[0.1.4]: https://pypi.org/project/updatable/0.1.4/
[0.1.3]: https://pypi.org/project/updatable/0.1.3/
[0.1.2]: https://pypi.org/project/updatable/0.1.2/
[0.1.1]: https://pypi.org/project/updatable/0.1.1/
[0.1.0]: https://pypi.org/project/updatable/0.1.0/
