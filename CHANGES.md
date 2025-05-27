# Version History

## Future Versions

 - N/A

## Upcoming Changes

- Dropped support for Python 3.7 and 3.8
- Added support for Python 3.13
- Fixed various Pylint warnings and errors:
  - Added encoding to `open()` calls
  - Replaced overly general exceptions with more specific ones
  - Removed unused imports
  - Fixed string formatting issues
  - Added missing `timeout` parameter in `requests.get()` to prevent potential infinite waits
  - Renamed parameter `license` to avoid conflict with built-in constant
- Update upload, lint and test workflows
- Add typing and documentation to the functions where it is missing
- Add workflow to check for new entries in CHANGES.md file
- Add CHANGES.md file

## Current Version

 - 2.0.5 (2024-01-11): Actions versions updated, supported Python versions updated, dependencies updated

## Past Versions

 - N/A
