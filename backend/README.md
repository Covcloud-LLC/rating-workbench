# Rating Workbench Backend

FastAPI-based microservice for the Rating Workbench application.

## Setup

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Code Quality

### Linting with Ruff

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting.

#### Check for Issues

```bash
# Check all files for linting issues
ruff check .

# Check specific files or directories
ruff check app/models/
ruff check app/services/policy_transaction_service.py
```

#### Auto-Fix Issues

```bash
# Automatically fix fixable issues
ruff check --fix .

# Fix and show what was changed
ruff check --fix --show-fixes .
```

#### Format Code

```bash
# Format all Python files
ruff format .

# Check formatting without making changes
ruff format --check .
```

#### Common Workflows

```bash
# Check and format in one go
ruff check --fix . && ruff format .

# Run before committing
ruff check . && ruff format --check . && pytest
```

### Ruff Configuration

Ruff is configured in `pyproject.toml` with the following enabled rule sets:
- **E/W**: pycodestyle errors and warnings
- **F**: pyflakes
- **I**: isort (import sorting)
- **N**: pep8-naming
- **UP**: pyupgrade
- **B**: flake8-bugbear
- **C4**: flake8-comprehensions
- **PL**: pylint
- And more...

See `pyproject.toml` for the complete configuration.

### Pre-commit Hooks (Optional)

To automatically run Ruff before each commit:

```bash
# From project root, install pre-commit (already in dev dependencies)
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

Once installed, Ruff will automatically check your code before each commit.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_mappers.py
```
