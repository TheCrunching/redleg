# Changelog

This is the changelog for RedLog a simple ledger application.

## [1.0.0-beta1] - 2025-07-16

Since no major bugs where found in [1.0.0-alpha1](#100-alpha1---2025-07-15) it became [1.0.0-beta1].

### Added

- Added a nice script to build the project
- Added LedgerFile.close() to explicitly close the file

### Changed

- Changed date for [1.0.0-alpha1](#100-alpha1---2025-07-15) it sayed the 16th even though it was released the 15

## [1.0.0-alpha1] - 2025-07-15

All right its time to release the first major version! But first I want to make sure everything is working well so we are going to be starting things off with an alpha release.

### Changed

- Moved ledger file code into its own class
- If ledger file empty create a blank ledger
- Changed Ctrl+c exit code [Exit codes](https://www.febooti.com/products/automation-workshop/online-help/actions/run-cmd-command/exit-codes/)

### Removed

- Removed verbosity argument

### Fixed

- Now when empty ledger created the json is indented 4 spaces

## [0.1.4] - 2025-07-15

0.1.4 adds some contributing guidelines and a couple code changes.

### Added

- Added contributing guidelines
- Added error handling when statement would be empty

## [0.1.3] - 2025-07-15

### Fixed

- Fixed bug where it would still fail if the path to the file was missing even after trying to create the file

### Changed

- Statements can be generated for years and months now
- Now give bug support back to version 3.4 of python

### Added

- Added a security policy
- Added a code of conduct

## [0.1.2] - 2025-07-14

### Added

- Added a command to generate monthly statements

### Changed

- Now the file location is not set

## [0.1.1] - 2025-07-14

### Fixed

- Fixed how I implemented the account equation

### Changed

- Changed the logging format
- Changed the date format

## [0.1.0] - 2025-07-13

_Initial release_

[0.1.0]: https://github.com/TheCrunching/RedLeg/releases/tag/v0.1.0
[0.1.1]: https://github.com/TheCrunching/RedLeg/releases/tag/v0.1.1
[0.1.2]: https://github.com/TheCrunching/RedLeg/releases/tag/v0.1.2
[0.1.3]: https://github.com/TheCrunching/RedLeg/releases/tag/v0.1.3
[0.1.4]: https://github.com/TheCrunching/RedLeg/releases/tag/v0.1.4
[1.0.0-alpha1]: https://github.com/TheCrunching/RedLeg/releases/tag/v1.0.0-alpha1
[1.0.0-beta1]: https://github.com/TheCrunching/RedLeg/releases/tag/v1.0.0-beta1
