# Contributing to EKS AI Troubleshooter

We welcome contributions to the EKS AI Troubleshooter! This document provides guidelines for contributing to the project.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/EKS-AI-Troubleshooter.git
   cd EKS-AI-Troubleshooter
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- AWS CLI configured
- Terraform >= 1.0
- Docker (optional)

### Local Development
```bash
# Setup Python environment
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run the application
python main.py
```

### Testing
```bash
# Run tests
pytest tests/

# Run linting
flake8 app/
black app/

# Type checking
mypy app/
```

## 📝 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Keep functions small and focused

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for adding tests

Example:
```
feat: add RAG-enhanced recommendations for OOMKilled pods

- Integrate sentence transformers for semantic search
- Add contextual solutions from knowledge base
- Improve recommendation accuracy by 40%
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update the README** if adding new features
5. **Create a detailed PR description**

### Areas for Contribution

#### 🧠 AI/ML Enhancements
- Improve RAG knowledge base with more sources
- Add predictive analytics for resource usage
- Implement anomaly detection algorithms
- Enhance natural language processing

#### 🔧 Infrastructure
- Add support for other Kubernetes distributions
- Implement multi-cloud support (GCP GKE, Azure AKS)
- Add Helm chart for easy deployment
- Improve cost optimization algorithms

#### 🌐 Frontend
- Enhance dashboard UI/UX
- Add mobile responsiveness
- Implement real-time notifications
- Add data visualization charts

#### 📊 Monitoring & Observability
- Add Prometheus metrics integration
- Implement custom alerting rules
- Add performance monitoring
- Enhance log analysis capabilities

#### 🛡️ Security
- Implement RBAC for multi-user access
- Add audit logging
- Enhance secret management
- Add vulnerability scanning

## 🐛 Bug Reports

When filing a bug report, please include:

1. **Environment details**:
   - OS and version
   - Python version
   - Kubernetes version
   - AWS region

2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Error logs** (if applicable)

## 💡 Feature Requests

For feature requests, please provide:

1. **Use case description**
2. **Proposed solution**
3. **Alternative solutions considered**
4. **Additional context**

## 📚 Documentation

Help improve our documentation:

- Fix typos and grammar
- Add examples and tutorials
- Improve API documentation
- Create video tutorials

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For security-related issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to EKS AI Troubleshooter! 🚀