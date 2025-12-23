# YggAPI Test Suite

Comprehensive test suite for the YggAPI qBittorrent Search Plugin.

## Running Tests

```bash
# From project root
python tests/test_yggapi.py

# Or with unittest
python -m unittest discover tests/

# Specific test file
python tests/test_yeeti_url_fetch.py
```

## Test Files

- **test_yggapi.py** - Main test suite (64 tests)

  - Configuration tests
  - URL caching tests
  - URL fetching tests
  - Search functionality tests
  - Integration tests
  - Edge case tests

- **test_yeeti_url_fetch.py** - Real network tests
  - Actual yeeti.io/@ygg fetching
  - URL pattern extraction
  - Cache functionality

## Test Coverage

- **64 tests** in main suite
- **~95% code coverage**
- All critical functionality tested
- Mocked external dependencies

## Documentation

See `/docs/TEST_GUIDE.md` for complete testing documentation.
