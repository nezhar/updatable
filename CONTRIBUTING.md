# Contributing

Thank you for your interest in contributing to this project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/nezhar/updatable.git
   cd updatable
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[test,dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running Tests

Run the test suite with coverage:
```bash
coverage run --source='./updatable' --omit='./updatable/__main__.py' run_tests.py
coverage report
```

## Code Quality

This project uses pre-commit hooks to ensure code quality. Run checks manually with:
```bash
pre-commit run --all-files
```

## Pull Requests

1. Fork the repository and create a new branch for your feature or fix.
2. Ensure all tests pass and code quality checks succeed.
3. Submit a pull request with a clear description of your changes.
