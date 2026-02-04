# api.duyet.net

[![CI/CD Pipeline](https://github.com/duyetdev/api.duyet.net/actions/workflows/ci.yml/badge.svg)](https://github.com/duyetdev/api.duyet.net/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

🚀 **Free Public API Service** - A collection of utility APIs for developers, providing gender detection, sentiment analysis, skill normalization, datetime parsing, and more.

[**Live Website**](https://api.duyet.net) | [**Documentation**](https://api.duyet.net) | [**Report Issues**](https://github.com/duyetdev/api.duyet.net/issues)

![api.duyet.net](screenshot.png)

## ✨ Features

- 🔍 **Gender Detection** - Predict gender from first names
- 😊 **Sentiment Analysis** - Analyze text sentiment (positive/negative/neutral)
- 🛠️ **Skill Normalization** - Clean and standardize technology/skill names
- 📅 **DateTime Parser** - Parse and normalize various datetime formats
- 👤 **Profile Generator** - Generate fake user profile data
- 🧠 **Neural Network Playground** - Interactive visualization of neural networks
- ⚡ **Rate Limited** - 5000 requests/day, 500 requests/hour per endpoint
- 🔒 **Secure** - HTTPS, security headers, input validation
- 📊 **Performance** - Response compression, optimized for speed
- 🎨 **Interactive Demos** - UI demo pages for each API

## 📋 Table of Contents

- [API Endpoints](#api-endpoints)
- [Quick Start](#quick-start)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Project Philosophy](#project-philosophy)
- [License](#license)

## 🌐 API Endpoints

### Gender Detection
```bash
GET /api/v1/gender?name=Emily

Response:
{
  "name": "Emily",
  "gender": "female",
  "time": 0.001
}
```

### Sentiment Analysis
```bash
GET /api/v1/senti?text=I love this!

Response:
{
  "probability": {
    "neg": 0.123,
    "neutral": 0.234,
    "pos": 0.643
  },
  "label": "pos"
}
```

### Skill Cleaning
```bash
GET /api/v1/clean_skill?skill=JavaScript

Response:
{
  "raw": "JavaScript",
  "cleaned": "js",
  "time": 0.002
}
```

### DateTime Parsing
```bash
GET /api/v1/clean_datetime?datetime=January 2020

Response:
{
  "raw": "January 2020",
  "cleaned": "2020-01-01",
  "time": 0.003
}
```

### Profile Generator
```bash
GET /api/v1/profile_faker

Response:
{
  "name": "John Doe",
  "email": "john@example.com",
  "address": "123 Main St",
  ...
}
```

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "service": "api.duyet.net",
  "version": "2.0.0"
}
```

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull and run
docker pull duyetdev/api-duyet
docker run -p 8080:8080 duyetdev/api-duyet

# Or build locally
docker build -t api-duyet .
docker run -p 8080:8080 api-duyet
```

Visit [http://localhost:8080](http://localhost:8080)

### Local Development

**Prerequisites:**
- Python 3.12+
- pip

**Setup:**

```bash
# Clone the repository
git clone https://github.com/duyetdev/api.duyet.net
cd api.duyet.net

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
export FLASK_DEBUG=true
python main.py
```

Visit [http://localhost:8080](http://localhost:8080)

## 🛠️ Development

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint
flake8
mypy .

# Security scan
bandit -r . -c pyproject.toml

# Run all pre-commit hooks
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_api_gender.py

# Run with verbose output
pytest -v
```

### Project Structure

```
api.duyet.net/
├── api/                    # API implementation modules
│   ├── gender.py          # Gender detection logic
│   ├── clean_skill.py     # Skill normalization
│   ├── clean_datetime.py  # DateTime parsing
│   ├── profile_faker.py   # Fake profile generation
│   └── utils.py           # Utility functions
├── templates/             # HTML templates
│   ├── index.html        # Main documentation page
│   ├── gender.html       # Gender API demo
│   ├── senti.html        # Sentiment API demo
│   └── nn/               # Neural network playground
├── static/               # Static assets (CSS, JS)
├── tests/                # Test suite
│   ├── conftest.py
│   ├── test_api_gender.py
│   ├── test_api_clean_skill.py
│   └── test_api_all.py
├── main.py               # Flask application entry point
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── app.yaml             # Google App Engine configuration
├── Dockerfile           # Docker configuration
├── pyproject.toml       # Tool configurations
└── .pre-commit-config.yaml  # Pre-commit hooks

```

## 🚢 Deployment

### Google App Engine

```bash
# Deploy to App Engine
gcloud app deploy

# View logs
gcloud app logs tail -s default

# Open in browser
gcloud app browse
```

### Docker

```bash
# Build image
docker build -t api-duyet:latest .

# Run container
docker run -d -p 8080:8080 --name api-duyet api-duyet:latest

# Push to registry
docker tag api-duyet:latest gcr.io/your-project/api-duyet:latest
docker push gcr.io/your-project/api-duyet:latest
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details and [CLAUDE.md](CLAUDE.md) for project philosophy and guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🆕 Request New API

Have an idea for a new API endpoint? [Create an issue](https://github.com/duyetdev/api.duyet.net/issues/new) with your suggestion!

## 📊 API Statistics

- **Rate Limits**: 5000 requests/day, 500 requests/hour per endpoint
- **Uptime**: 99.9%+
- **Response Time**: < 100ms average
- **Free Forever**: No API keys required

## 🔒 Security

- All external API calls use HTTPS
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Input validation on all endpoints
- Regular security scanning with Bandit
- Rate limiting to prevent abuse

## 🏗️ Technology Stack

- **Backend**: Flask 3.1.2, Python 3.12
- **Deployment**: Google App Engine
- **Web Server**: Gunicorn
- **Testing**: Pytest
- **Code Quality**: Black, Flake8, MyPy, Bandit
- **Frontend**: TypeScript, D3.js, Material Design Lite
- **CI/CD**: GitHub Actions

## 📝 Changelog

### Version 2.0.0 (2024)
- 🎉 **Major Update**: Migrated from Python 2.7 to Python 3.12
- 🔒 Security improvements (HTTPS, headers, input validation)
- ⚡ Performance optimization (compression, caching)
- 🧪 Added comprehensive test suite (pytest)
- 📚 Improved documentation and API responses
- 🐳 Docker support for local development
- 🔧 Modern development tooling (Black, MyPy, pre-commit)
- 🤖 CI/CD pipeline with GitHub Actions

### Version 1.0.0
- Initial release with basic API endpoints

## 🎯 Project Philosophy

This project follows a clear set of principles and guidelines documented in [CLAUDE.md](CLAUDE.md).

**Core Values:**
- **Free & Accessible** - No API keys, generous rate limits
- **Developer-First** - Helpful errors, clear docs, fast responses
- **Production-Grade** - Secure, tested, modern practices

**Key Principles:**
- Keep it simple, but not simpler
- Every error is an opportunity to teach
- Security is not optional
- Clarity over cleverness

For detailed architecture principles, code style guidelines, security best practices, and lessons learned from past bugs, see [CLAUDE.md](CLAUDE.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Van-Duyet Le** ([@duyetdev](https://github.com/duyetdev))

- Website: [duyet.net](https://duyet.net)
- Twitter: [@duyetdev](https://twitter.com/duyetdev)
- GitHub: [@duyetdev](https://github.com/duyetdev)

## ⭐ Support

If you find this project useful, please give it a ⭐ star on GitHub!

## 🙏 Acknowledgments

- Neural Network Playground based on [TensorFlow Playground](https://playground.tensorflow.org/)
- Thanks to all contributors who have helped improve this project
- Built with ❤️ for the developer community

---

Made with ❤️ by [duyet.net](https://duyet.net)
