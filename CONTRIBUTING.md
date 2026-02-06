# Contributing to Time-Horizon Protocol

Thank you for your interest in contributing! This project was born from multi-AI collaboration and welcomes contributions from humans and AI-assisted workflows alike.

## 🎯 Ways to Contribute

### 1. Report Issues
Found a bug? Have a feature request?

- Check [existing issues](https://github.com/TimeHorizonProtocol/Time-Horizon-Protocol/issues) first
- Open a new issue with a clear title and description
- Include error messages, code snippets, or screenshots if relevant

### 2. Improve Documentation
- Fix typos or unclear explanations
- Add examples or use cases
- Translate documentation to other languages

### 3. Contribute Code
- Bug fixes
- New features (discuss in an issue first!)
- Performance improvements
- Test coverage

### 4. Research & Analysis
- Backtest on historical market events
- Integrate real APIs (GDELT, Twitter, market data)
- Write academic papers or blog posts referencing the project

---

## 🔧 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/Time-Horizon-Protocol.git
cd Time-Horizon-Protocol

# 3. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run tests (once available)
pytest

# 6. Try the demo
python time_horizon_v2.py
```

---

## 📝 Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints where possible
- Add docstrings to all public functions/classes
- Keep functions focused and modular
- Comment complex logic

### Example:
```python
async def calculate_stress(market_data: MarketData) -> float:
    """
    Calculate normalized market stress level.
    
    Args:
        market_data: Current market snapshot
        
    Returns:
        Stress level between 0.0 and 1.0
    """
    # Implementation...
```

---

## 🔄 Pull Request Process

1. **Create a branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, atomic commits
   - Test your changes thoroughly

3. **Commit with descriptive messages**
   ```bash
   git commit -m "Add GDELT API integration for geopolitical risk"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Describe what changed and why
   - Reference related issues (e.g., "Fixes #42")
   - Be patient - maintainers review as time allows

---

## 🧪 Testing Guidelines

**Coming soon:** We're building a comprehensive test suite.

For now, please:
- Test your code manually before submitting
- Include example usage in your PR description
- Note any edge cases or limitations

---

## 📊 Priority Areas

Help is especially appreciated in these areas:

### High Priority
- [ ] Real API integration (Twitter/X, GDELT, market data feeds)
- [ ] Comprehensive backtesting framework
- [ ] Unit tests and integration tests
- [ ] Performance optimization

### Medium Priority
- [ ] Web dashboard (Flask/Streamlit)
- [ ] Visualization tools (charts, graphs)
- [ ] Configuration GUI
- [ ] Docker containerization

### Research
- [ ] Academic paper for peer review
- [ ] Comparison with existing circuit breaker systems
- [ ] Game theory analysis (can the system be gamed?)

---

## 🤝 Code of Conduct

### Our Standards

**We encourage:**
- Constructive feedback
- Respect for different perspectives
- Collaboration over competition
- Learning from mistakes

**We don't tolerate:**
- Harassment or discriminatory behavior
- Spam or self-promotion without value
- Plagiarism or copyright violations

This project emerged from AI collaboration - we believe good ideas can come from anywhere. Everyone is welcome.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0 (same as the project).

---

## 💬 Questions?

- **GitHub Issues:** For bugs and feature requests
- **Discussions:** For general questions and ideas
- **Email:** [Coming soon]

---

## 🙏 Acknowledgments

Special thanks to:
- The AI models (ChatGPT, Gemini, DeepSeek, Grok & Claude) whose collaboration made this possible
- All contributors who help improve financial market stability
- The open-source community

---

**Thank you for making markets more resilient!** 🚀
