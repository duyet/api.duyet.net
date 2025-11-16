# CLAUDE.md - Project Philosophy & Guidelines

> **"Technology alone is not enough. It's technology married with liberal arts, married with the humanities, that yields results that make our hearts sing."** - Steve Jobs

This document serves as the philosophical foundation and technical guide for **api.duyet.net**. It's written for AI assistants, developers, and future maintainers who want to understand and preserve the soul of this project.

---

## 🎯 Project Vision

**api.duyet.net** is more than just a collection of API endpoints—it's a **gift to the developer community**. Every design decision reflects these core values:

### 1. **Free & Accessible**
- **No API keys required** - Zero friction for developers
- **Generous rate limits** - 5000 requests/day, 500/hour per endpoint
- **Simple REST API** - Clean, intuitive endpoints
- **Interactive demos** - Every API has a visual playground

### 2. **Developer-First Experience**
- **Helpful error messages** - Don't just say "error", explain what happened and how to fix it
- **Examples in responses** - Show users how to use the API correctly
- **Comprehensive docs** - README with clear examples
- **Fast response times** - < 100ms average

### 3. **Production-Grade Quality**
- **Security hardened** - HTTPS, headers, input validation
- **Tested thoroughly** - Comprehensive test coverage
- **Modern practices** - Python 3.12, type hints, logging
- **Monitored** - Health checks, proper error handling

---

## 🏗️ Architecture Principles

### **Keep It Simple, But Not Simpler**

This project follows Einstein's principle: "Everything should be made as simple as possible, but not simpler."

```python
# ✅ GOOD: Simple, clear, helpful
if not name or not name.strip():
    return jsonify(
        error="Missing parameter",
        message="Please provide 'name' parameter",
        example="/api/v1/gender?name=John"
    ), 400

# ❌ BAD: Too simple, not helpful
if not name:
    return jsonify(message='error')
```

### **Every Error is an Opportunity to Teach**

When something goes wrong, we don't just report it—we **guide the user toward success**.

```python
# ✅ GOOD: Educational error message
return jsonify(
    error="Rate limit exceeded",
    message="You've made too many requests",
    suggestion="Please wait before making more requests",
    retry_after=3600
), 429

# ❌ BAD: Cryptic error
return "ratelimit exceeded", 429
```

### **Security is Not Optional**

- Always use **HTTPS** for external calls
- Always **validate input** before processing
- Always **sanitize output** before returning
- Never expose **internal errors** to users
- Never trust **user input**

### **Performance Matters, But Clarity Matters More**

```python
# ✅ GOOD: Clear and fast enough
gender = 'female' if any(s.lower() in name for s in female_name) else 'unknown'

# ❌ BAD: Fast but incomprehensible
gender = 'female' if (s.lower() in name for s in female_name) else 'unknown'  # BUG!
```

---

## 🎨 Code Style Philosophy

### **Python 3.12+ Modern Practices**

1. **Use Type Hints** (when they add clarity)
   ```python
   def clean_skill(skill: str, remove_stopwords: bool = True) -> str:
       """Clean and normalize skill names."""
   ```

2. **Use F-Strings** (always)
   ```python
   logger.info(f"Clean skill: {skill} -> {result}")  # ✅ GOOD
   logger.info("Clean skill: %s -> %s" % (skill, result))  # ❌ OLD
   ```

3. **Use Logging** (not print)
   ```python
   logger.error(f"Gender API error: {str(e)}")  # ✅ GOOD
   print(result, skill)  # ❌ NEVER
   ```

4. **Use Specific Exceptions** (not bare except)
   ```python
   try:
       result = process(data)
   except ValueError as e:  # ✅ GOOD
       logger.error(f"Invalid data: {e}")

   # ❌ NEVER use bare except
   except:
       pass
   ```

### **Black Formatting**

This project uses **Black** with 100-character line length.

```bash
# Format all code
black .

# Check formatting
black --check .
```

**Why Black?** Because arguing about code style is a waste of time. Let Black handle it.

### **Docstrings Matter**

Every function should explain **what it does** and **why it exists**.

```python
def name_to_gender(name: str) -> str:
    """Predict gender from first name using female name database.

    This is a simple heuristic classifier that checks if a name
    appears in our female names dataset. If not found, defaults
    to 'male'. This is obviously imperfect and culturally biased,
    but serves as a reasonable first approximation.

    Args:
        name: First name to analyze

    Returns:
        str: 'female', 'male', or 'unknown'
    """
```

---

## 🧪 Testing Philosophy

### **Every API Endpoint Needs Tests**

When you add a new endpoint, you **must** add tests:

```python
class TestMyNewAPI:
    """Test suite for /api/v1/my_endpoint."""

    def test_success_case(self, client):
        """Test the happy path."""
        response = client.get('/api/v1/my_endpoint?param=value')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data

    def test_missing_parameter(self, client):
        """Test missing parameter handling."""
        response = client.get('/api/v1/my_endpoint')
        assert response.status_code == 400

    def test_invalid_input(self, client):
        """Test invalid input handling."""
        response = client.get('/api/v1/my_endpoint?param=invalid')
        assert response.status_code == 400
```

### **Test Coverage ≥ 80%**

We aim for **80%+ test coverage**. Not because it's a magic number, but because:
- It catches regressions
- It documents behavior
- It gives confidence to refactor

```bash
pytest --cov --cov-report=term-missing
```

---

## 🔒 Security Guidelines

### **The Security Checklist**

Before deploying **any** code, verify:

- [ ] All external API calls use **HTTPS** (not HTTP)
- [ ] All user input is **validated**
- [ ] All error messages are **safe** (no stack traces in production)
- [ ] All sensitive data is **logged securely** (no passwords in logs)
- [ ] All endpoints have **rate limiting**
- [ ] All responses have **security headers**

### **Common Vulnerabilities to Avoid**

1. **Command Injection**
   ```python
   # ❌ DANGEROUS
   os.system(f"echo {user_input}")

   # ✅ SAFE
   subprocess.run(["echo", user_input], check=True)
   ```

2. **SQL Injection** (if we ever add a database)
   ```python
   # ❌ DANGEROUS
   cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")

   # ✅ SAFE
   cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
   ```

3. **XSS** (Cross-Site Scripting)
   ```python
   # Always validate and sanitize input
   # Always escape output
   # Use Content-Security-Policy headers
   ```

---

## 📦 Dependency Management

### **Production Dependencies** (`requirements.txt`)
- Keep **minimal** - only what's needed to run
- Pin **major versions** - e.g., `flask==3.1.2`
- Update **regularly** - check for security patches weekly

### **Development Dependencies** (`requirements-dev.txt`)
- Include **all tools** - testing, linting, formatting
- Keep **up to date** - latest versions unless incompatible

### **The Upgrade Process**

```bash
# 1. Update dependencies
pip install --upgrade -r requirements.txt

# 2. Run tests
pytest

# 3. Check for security issues
bandit -r .
safety check

# 4. Update lockfile
pip freeze > requirements.txt
```

---

## 🚀 Deployment Philosophy

### **Environment-Based Configuration**

Never hardcode **anything** that varies by environment:

```python
# ✅ GOOD
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# ❌ BAD
DEBUG = True
```

### **The Deployment Checklist**

Before deploying to production:

- [ ] All tests pass (`pytest`)
- [ ] Code is formatted (`black --check .`)
- [ ] No linting errors (`flake8`)
- [ ] No security issues (`bandit -r .`)
- [ ] No type errors (`mypy .` - if applicable)
- [ ] `DEBUG=False` in production
- [ ] All logs use proper levels (INFO, WARNING, ERROR)
- [ ] Rate limits are configured
- [ ] Health check works (`/health`)

---

## 🎓 Learning from Mistakes

### **The Gender API Bug (2024)**

**What Happened:**
```python
# BUG - generator expression always evaluates to True
gender = 'female' if (s.lower() in name for s in female_name) else 'unknown'
```

**The Fix:**
```python
# FIXED - use any() to properly evaluate
gender = 'female' if any(s.lower() in name for s in female_name) else 'unknown'
```

**Lessons Learned:**
1. Always test your logic with real data
2. Generator expressions are not boolean checks
3. Tests would have caught this immediately

### **The HTTP Sentiment API (2024)**

**What Happened:**
```python
# SECURITY ISSUE - unencrypted HTTP call
url='http://text-processing.com/api/sentiment/'
```

**The Fix:**
```python
# FIXED - use HTTPS
response = requests.post(
    'https://text-processing.com/api/sentiment/',
    data=form_data,
    headers=headers,
    timeout=10
)
```

**Lessons Learned:**
1. Always use HTTPS for external APIs
2. Security scanners should catch this (Bandit does now)
3. Never trust default configurations

---

## 🌟 The Developer Experience Mindset

When making **any** change, ask yourself:

1. **Will this confuse users?**
   - If yes, add documentation or improve the API design

2. **Will this break existing code?**
   - If yes, is the breaking change worth it? Can we make it backward compatible?

3. **Will future maintainers understand this?**
   - If no, add comments or refactor for clarity

4. **Is this the simplest solution?**
   - If no, simplify it

5. **Does this make the project better?**
   - If no, don't do it

---

## 🔧 Common Tasks

### **Adding a New API Endpoint**

1. **Create the function** in `api/my_feature.py`
2. **Add the route** in `main.py`
3. **Add rate limiting** decorators
4. **Add input validation** with helpful errors
5. **Add logging** for debugging
6. **Create tests** in `tests/test_api_my_feature.py`
7. **Create demo page** in `templates/my_feature.html`
8. **Update documentation** in `README.md`

### **Fixing a Bug**

1. **Write a failing test** that reproduces the bug
2. **Fix the code** until the test passes
3. **Run all tests** to ensure no regressions
4. **Update documentation** if behavior changed
5. **Commit with clear message** explaining the fix

### **Improving Performance**

1. **Measure first** - don't optimize blindly
2. **Add caching** if appropriate
3. **Use compression** for large responses
4. **Optimize database queries** (if applicable)
5. **Add monitoring** to track improvements

---

## 📚 Recommended Reading

- [The Zen of Python](https://www.python.org/dev/peps/pep-0020/) - Beautiful is better than ugly
- [The Twelve-Factor App](https://12factor.net/) - Best practices for web apps
- [API Design Guidelines](https://cloud.google.com/apis/design) - Google's API standards
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)

---

## 🤝 Contributing Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

**Key Principles:**
- Code should be **self-documenting**
- Tests should be **comprehensive**
- Commits should be **atomic and clear**
- PRs should be **focused and reviewable**

---

## 🎯 Success Metrics

How do we know if we're doing well?

- ✅ **Response time** < 100ms average
- ✅ **Uptime** > 99.9%
- ✅ **Test coverage** > 80%
- ✅ **Security scan** passes with 0 high/critical issues
- ✅ **User satisfaction** measured by GitHub stars and issues

---

## 💡 Remember

> **"Simplicity is the ultimate sophistication."** - Leonardo da Vinci

When in doubt:
- Choose **clarity** over cleverness
- Choose **security** over convenience
- Choose **user experience** over implementation ease
- Choose **tests** over "trust me, it works"

---

## 🙏 Final Words

This project is a **labor of love** for the developer community. Every line of code, every test, every documentation page is written with **care and intention**.

Treat it with respect. Make it better. Leave it better than you found it.

When you add code, ask: **"Will developers love using this?"**

If the answer is yes, ship it. If not, make it better.

---

**Made with ❤️ for developers, by developers.**

*Last updated: 2024 - Python 3.12 Migration*
