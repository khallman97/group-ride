# Tests for Group Fitness API

This directory contains comprehensive tests for the Group Fitness API backend.

## Test Structure

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Pytest configuration and fixtures
├── test_auth.py             # Authentication API and service tests
├── test_users.py            # Users API and service tests
├── test_group_events.py     # Group Events API and service tests
└── README.md                # This file
```

## Test Categories

### 1. Authentication Tests (`test_auth.py`)
- **API Tests**: Test authentication endpoints
  - Health check
  - User info retrieval
  - Token validation
  - Token refresh
  - Logout
- **Service Tests**: Test AuthService methods
  - User info retrieval from Cognito
  - Token validation
  - Token refresh
  - Error handling
- **Dependency Tests**: Test authentication dependencies
  - Current user retrieval
  - Invalid token handling

### 2. Users Tests (`test_users.py`)
- **API Tests**: Test user management endpoints
  - Profile retrieval and updates
  - Preferences management
  - User onboarding
  - Authentication requirements
- **Service Tests**: Test UserService methods
  - Profile CRUD operations
  - Preferences management
  - Data validation

### 3. Group Events Tests (`test_group_events.py`)
- **API Tests**: Test group events endpoints
  - Event creation (with authentication)
  - Event retrieval (public)
  - Single event retrieval
  - Data validation
- **Service Tests**: Test GroupEventService methods
  - Event CRUD operations
  - Data ordering
  - Error handling

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### Basic Test Commands

Run all tests:
```bash
python run_tests.py
```

Run specific test categories:
```bash
python run_tests.py --auth          # Authentication tests only
python run_tests.py --users         # User tests only
python run_tests.py --group-events  # Group events tests only
```

Run with coverage:
```bash
python run_tests.py --coverage
```

Run with verbose output:
```bash
python run_tests.py --verbose
```

### Using pytest directly

Run all tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run specific test class:
```bash
pytest tests/test_auth.py::TestAuthAPI
```

Run specific test method:
```bash
pytest tests/test_auth.py::TestAuthAPI::test_health_check
```

Run with markers:
```bash
pytest -m auth          # Run auth-related tests
pytest -m users         # Run user-related tests
pytest -m group_events  # Run group events tests
pytest -m "not slow"    # Skip slow tests
```

## Test Configuration

### Fixtures (`conftest.py`)
- `db_engine`: SQLite in-memory database engine
- `db_session`: Database session for each test
- `client`: FastAPI test client with test database
- `test_user_data`: Sample user data
- `test_group_event_data`: Sample group event data
- `mock_auth_token`: Mock authentication token
- `mock_user_info`: Mock user information

### Database Testing
Tests use an in-memory SQLite database to ensure:
- Fast test execution
- No external dependencies
- Clean state for each test
- Automatic cleanup

### Authentication Mocking
Authentication is mocked in tests to:
- Avoid external AWS Cognito calls
- Test authentication flows independently
- Provide consistent test data

## Test Coverage

The test suite covers:
- ✅ API endpoint functionality
- ✅ Service layer business logic
- ✅ Database operations
- ✅ Authentication flows
- ✅ Error handling
- ✅ Data validation
- ✅ Authorization checks

## Adding New Tests

### For New API Endpoints
1. Add API tests in the appropriate test file
2. Test both success and failure scenarios
3. Test authentication requirements
4. Test data validation

### For New Services
1. Add service tests in the appropriate test file
2. Test all public methods
3. Test error conditions
4. Mock external dependencies

### For New Models
1. Test model creation and relationships
2. Test database constraints
3. Test field validation

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear, descriptive test names
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **Mock External Dependencies**: Don't rely on external services
5. **Test Edge Cases**: Include error conditions and edge cases
6. **Use Fixtures**: Reuse common test data and setup

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 30 seconds for full suite)
- No external dependencies
- Clear pass/fail results
- Coverage reporting
- Parallel execution support
