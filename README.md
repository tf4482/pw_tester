# 🔐 pw_tester

A comprehensive password security analysis tool with both command-line and web interfaces. Analyzes password complexity and estimates brute force attack times with professional visualizations.

## ✨ Features

### 🖥️ Command Line Interface
- **🔑 Interactive Asterisk Input**: Secure password entry with visual feedback (*)
- **🎨 Colorized Output**: Beautiful console output with colors and emojis
- **📊 Password Complexity Analysis**: Evaluates character space, entropy, and overall strength
- **⚡ Brute Force Time Estimation**: Calculates attack times for 5 different scenarios
- **💡 Security Recommendations**: Provides actionable advice to improve password strength
- **🌍 Cross-Platform Support**: Works on Windows, Linux, and macOS
- **🎯 Demo Mode**: Examples with different password types

### 🌐 Web Interface
- **🎨 Modern UI**: Beautiful Tailwind CSS interface with responsive design
- **🌙 Dark Mode**: Toggle between light and dark themes with persistent preference
- **🔒 Secure Analysis**: Real-time password analysis without storage
- **📱 Mobile Friendly**: Works perfectly on all devices
- **⚡ Fast API**: RESTful API for password analysis
- **🎯 Demo Examples**: Interactive demo with various password types
- **🏭 Production Ready**: Gunicorn WSGI server configuration

## � Installation

### 🚀 Using Poetry (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd pw_tester

# Install dependencies
poetry install

# Run the tool
poetry run pw-tester
```

### 🐍 Direct Python Usage

```bash
# Run directly with Python
python3 pw_tester.py
```

## 🎮 Usage

### 🖥️ Command Line Interface

```bash
# Interactive mode (default) - secure asterisk input
pw_tester.py

# Demo mode with examples
pw_tester.py --demo

# Show password in output
pw_tester.py --show-password

# Help
pw_tester.py --help
```

### 🌐 Web Interface

```bash
# Development server
poetry run python web_app.py

# Production server with Gunicorn
poetry run gunicorn --config gunicorn.conf.py web_app:app

# Using Poetry script
poetry run pw-tester-web
```

**Web Interface URLs:**
- **Main Interface**: `http://localhost:5000/`
- **Demo Page**: `http://localhost:5000/demo`
- **API Health Check**: `http://localhost:5000/api/health`
- **Password Analysis API**: `POST http://localhost:5000/api/analyze`

### 🔌 API Usage

```bash
# Analyze a password via API
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"password":"your_password_here"}'

# Get demo examples
curl http://localhost:5000/api/demo
```

### Example Output

The tool provides colorized output with emojis for better visual experience:

```
🔐              PW_TESTER ANALYSIS              🔐
============================================================

📊 PASSWORD PROPERTIES:
  Length:          17 characters
  Character space: 88 possible characters
  Entropy:         108.61 bits
  Complexity:      Strong (colored based on strength)
  Combinations:    1,138,165,524,602,471,949,554,948,880,990,208

⚡ BRUTE FORCE TIME ESTIMATES:
  💻 Basic CPU (1M/s)         : Practically uncrackable (> 1000 years)
  🖥️  Modern CPU (100M/s)    : Practically uncrackable (> 1000 years)
  🎮 Single GPU (10B/s)       : Practically uncrackable (> 1000 years)
  🔥 GPU Cluster (1T/s)       : Practically uncrackable (> 1000 years)
  🚀 Quantum Computer (1P/s)  : Practically uncrackable (> 1000 years)

💡 RECOMMENDATIONS:
  ✅ Your password has good complexity!
============================================================
```

## ⚡ Attack Scenarios

| Emoji | Scenario | Speed | Description |
|-------|----------|-------|-------------|
| 💻 | Basic CPU | 1M/s | Single-threaded CPU attack |
| 🖥️ | Modern CPU | 100M/s | Multi-core CPU with optimizations |
| 🎮 | Single GPU | 10B/s | High-end graphics card |
| 🔥 | GPU Cluster | 1T/s | Multiple GPUs in parallel |
| 🚀 | Quantum Computer | 1P/s | Theoretical future quantum attacks |

## 📈 Complexity Scoring

Password strength is rated based on entropy:

- **🔴 Very Weak**: < 28 bits
- **🟠 Weak**: 28-36 bits
- **🟡 Medium**: 36-60 bits
- **🟢 Strong**: 60-128 bits
- **💚 Very Strong**: > 128 bits

## 🔤 Character Sets

- **🔤 Lowercase**: a-z (26 characters)
- **🔠 Uppercase**: A-Z (26 characters)
- **🔢 Digits**: 0-9 (10 characters)
- **🔣 Special**: !@#$%^&*()_+-=[]{}|;:,.<>? (28 characters)
- **⎵ Space**: (1 character)

## 🔍 Pattern Detection

The analyzer detects and penalizes common weak patterns:

- 🔢 Consecutive numbers (1234, 5678)
- 🔤 Consecutive letters (abcd, wxyz)
- 🔁 Repeated characters (aaa, 111)
- 📝 Common sequences and patterns

## 🛠️ Development

### 🧪 Running Tests

```bash
# With Poetry
poetry run pytest

# Direct Python
python3 -m pytest test_pw_tester.py
```

### ✨ Code Quality

```bash
# Format code
poetry run black pw_tester.py web_app.py

# Lint code
poetry run flake8 pw_tester.py web_app.py

# Type checking
poetry run mypy pw_tester.py web_app.py
```

### 🌐 Web Development

```bash
# Run development server
FLASK_ENV=development poetry run python web_app.py

# Run production server
poetry run gunicorn --config gunicorn.conf.py web_app:app

# Test API endpoints
curl http://localhost:5000/api/health
```

## 🛡️ Security

- **🚫 No Password Storage**: Passwords are never stored or logged (CLI & Web)
- **🧠 Memory Safety**: Passwords are processed in memory only
- **🔒 Secure Transmission**: Web interface uses HTTPS in production
- **⚖️ Conservative Estimates**: Brute force times assume average case (50% of keyspace)
- **🔍 Pattern Recognition**: Common attack patterns are considered in entropy calculation
- **🏭 Production Security**: Gunicorn configuration with security best practices

## 📄 License

This project is open source.

## 🚀 Production Deployment

### 🏭 Using Gunicorn

```bash
# Install dependencies
poetry install

# Run with Gunicorn
poetry run gunicorn --config gunicorn.conf.py web_app:app

# Or with custom settings
poetry run gunicorn -w 4 -b 0.0.0.0:5000 web_app:app
```

### 🌍 Environment Variables

```bash
# Production settings
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here
export PORT=5000
export WEB_CONCURRENCY=4
export LOG_LEVEL=info
```

## ⚠️ Disclaimer

This tool is for educational and security assessment purposes. The time estimates are theoretical and may vary based on actual attack implementations, hardware capabilities, and other factors. Always use strong, unique passwords and consider additional security measures like multi-factor authentication.
