# Contributing to api.duyet.net

Thank you for your interest in contributing to api.duyet.net! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.12 or higher
- pip and virtualenv
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/duyetdev/api.duyet.net.git
   cd api.duyet.net
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run the development server**
   ```bash
   export FLASK_DEBUG=true
   python main.py
   ```

   Or with Docker:
   ```bash
   docker build -t api-duyet .
   docker run -p 8080:8080 api-duyet
   ```

## Code Style

This project uses:
- **Black** for code formatting (line length: 100)
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking
- **bandit** for security scanning

Run all checks:
```bash
black .
isort .
flake8
mypy .
bandit -r . -c pyproject.toml
```

Or use pre-commit to run all checks automatically:
```bash
pre-commit run --all-files
```

## Testing

Write tests for all new features and bug fixes.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_api_gender.py
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and checks**
   ```bash
   pytest
   pre-commit run --all-files
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting, etc.)
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all CI checks pass

## Adding a New API Endpoint

1. Create the API function in the `api/` directory
2. Add the route in `main.py`
3. Add input validation and error handling
4. Add rate limiting decorators
5. Create a demo HTML page in `templates/`
6. Write tests in `tests/`
7. Update the main `index.html` documentation

Example:
```python
# api/my_new_api.py
def my_new_function(input_data: str) -> dict:
    """Process the input data.

    Args:
        input_data: The data to process

    Returns:
        dict: Processed result
    """
    # Implementation
    return {"result": input_data.upper()}

# main.py
@app.route('/api/v1/my_endpoint')
@limiter.limit("5000 per day")
@limiter.limit("500 per hour")
def my_endpoint_api():
    """My new API endpoint."""
    data = request.args.get('data', '')

    if not data:
        return jsonify(error="Missing parameter"), 400

    try:
        result = my_new_function(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify(error="Internal error"), 500
```

## Reporting Issues

- Use the GitHub issue tracker
- Include detailed description
- Provide steps to reproduce
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a professional environment

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
