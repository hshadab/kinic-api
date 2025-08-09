# Kinic Automation Suite

Transform your Kinic Chrome extension into a powerful API with desktop app - no coding required!

> **🔗 Kinic is an on-chain vector database** - enabling verifiable, decentralized, and immutable knowledge storage for AI agents and collaborative development.

### Why Kinic vs Traditional RAG/Memory Solutions?
Unlike cloud-based memory APIs that charge per call and lock your data in proprietary silos:
- **✅ You Own Your Data** - On-chain storage means no vendor lock-in, no API fees
- **✅ Cross-Platform Memory** - Works across ALL your AI agents, not just one provider
- **✅ Zero Marginal Cost** - After initial storage, unlimited queries without per-call charges
- **✅ Composable & Interoperable** - Any agent/app can access the same memory layer
- **✅ Censorship Resistant** - No provider can suddenly restrict or delete your knowledge
- **✅ Privacy First** - Your memory stays yours, not training someone else's models

> **📚 Full API Documentation:** See [API-DOCUMENTATION.md](API-DOCUMENTATION.md) for complete v5 API implementation details, including search-and-retrieve URLs and AI text extraction features.

## 🚀 Quick Start - Download Desktop App

Get started in 30 seconds with our user-friendly desktop application:

### Direct Downloads (Latest Build):
[![Download for Windows](https://img.shields.io/badge/Download-Windows-blue?style=for-the-badge&logo=windows)](https://nightly.link/ICME-Lab/kinic-api/workflows/build-desktop/main/KinicDesktop-Windows.zip)
[![Download for macOS](https://img.shields.io/badge/Download-macOS-black?style=for-the-badge&logo=apple)](https://nightly.link/ICME-Lab/kinic-api/workflows/build-desktop/main/KinicDesktop-macOS.zip)

> **Direct downloads powered by [nightly.link](https://nightly.link)** - No GitHub login required!
> 
> Alternative: [View all builds](https://github.com/ICME-Lab/kinic-api/actions/workflows/build-desktop.yml) on GitHub Actions

### Three Simple Steps:
1. **Download** - Click your platform above
2. **Setup** - Run app and click "Setup Kinic Position" (hover over icon for 5 seconds)
3. **Use** - Click buttons or start API server for integrations!

No terminal. No Python. No complexity. Just works! ✨

---

## 📁 Project Structure

```
kinic/
├── kinic-api/          # Main desktop app & API (actively maintained)
│   ├── kinic-desktop.py    # GUI application
│   ├── kinic-api.py        # Core API functionality
│   └── examples/           # Integration examples
└── kinic-axiom/        # Axiom.ai integration (experimental)
```

## ✨ Features

### Desktop Application
- **🖱️ Visual Setup** - No typing coordinates, just point and click
- **📍 System Tray** - Runs quietly in background, always accessible
- **⚡ Quick Actions** - One-click save & search buttons
- **🔧 Built-in API** - Start/stop API server with a button
- **🚀 Auto-start** - Launch with your computer (optional)

### 🎯 Inspiring Use Cases

#### 🔗 On-Chain Vector Database Powers
Leverage Kinic's blockchain foundation for verifiable, decentralized AI memory:
- **Verifiable AI Training** - Cryptographic proof of what data your AI learned from
- **Knowledge DAOs** - Teams share discoveries with on-chain attribution and incentives
- **Proof of Debug** - Build reputation with immutable problem-solving history
- **Zero-Knowledge Code Reviews** - Learn from others' code without seeing proprietary details

#### 🧠 Persistent Shared Memory Magic
Transform how AI agents and developers collaborate across sessions:
- **Multi-Agent Hive Mind** - AI agents that share discoveries and learn collectively
- **Context Resurrection** - Instantly restore your mental state when returning to projects
- **Rubber Duck with Memory** - Debugging assistant that recalls all past conversations
- **Cross-Session Learning** - Your AI gets smarter by remembering what worked
- **Living Documentation** - Docs that evolve based on actual code usage
- **Predictive Debugging** - Anticipate bugs based on historical patterns
- **Code Pattern Mining** - Discover patterns across all your projects automatically
- **Self-Improving Reviews** - AI that learns from accepted/rejected suggestions

### API Endpoints (v5)
Transform Kinic into a powerful API for your workflows:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/save` | POST | Save current page to Kinic |
| `/search` | POST | Search your Kinic memory |
| `/search-and-retrieve` | POST | Search and get first URL |
| `/search-ai-extract` | POST | Search with AI analysis extraction |
| `/click` | POST | Open Kinic extension |
| `/close` | POST | Close Kinic extension |
| `/setup-kinic` | POST | Configure Kinic button position |
| `/setup-ai` | POST | Configure AI response position |

## 🛠️ Integration Examples

### Zapier / Make / n8n
```javascript
// Webhook action
POST http://localhost:5000/api/save
{
  "url": "https://example.com"
}
```

### Python Script
```python
import requests

# Save a page
requests.post('http://localhost:5000/api/save', 
    json={'url': 'https://arxiv.org/paper'})

# Search memories
result = requests.post('http://localhost:5000/api/search', 
    json={'query': 'machine learning transformers'})
```

### Command Line
```bash
# Quick save
curl -X POST http://localhost:5005/save

# Search and get URL
curl -X POST http://localhost:5005/search-and-retrieve \
  -H "Content-Type: application/json" \
  -d '{"query": "python tutorial"}'

# Search with AI text extraction
curl -X POST http://localhost:5005/search-ai-extract \
  -H "Content-Type: application/json" \
  -d '{"query": "summarize my research on LLMs"}'
```

## 🔧 Advanced Usage

### For Developers (Python Script)
If you prefer the command-line version:

```bash
git clone https://github.com/ICME-Lab/kinic-api.git
cd kinic-api
pip install -r requirements.txt
python kinic-api.py
```

### API Authentication (Optional)
Set an API key for security:
```bash
export KINIC_API_KEY="your-secret-key"
```

Then include in requests:
```python
headers = {'X-API-Key': 'your-secret-key'}
```

## 📋 Requirements

- Chrome browser installed
- [Kinic Chrome extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc) installed
- Operating System: Windows 10+ or macOS 10.14+

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs or request features via [Issues](https://github.com/ICME-Lab/kinic-api/issues)
- Submit pull requests
- Share your integration examples

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/ICME-Lab/kinic-api/wiki)
- **Issues**: [Bug Reports](https://github.com/ICME-Lab/kinic-api/issues)
- **Discussions**: [Community Forum](https://github.com/ICME-Lab/kinic-api/discussions)

## 🙏 Acknowledgments

Built with ❤️ for the Kinic community. Special thanks to all contributors and users who provided feedback to make this tool better.

---

<p align="center">
  <strong>Ready to supercharge your Kinic workflow?</strong><br>
  <a href="https://github.com/ICME-Lab/kinic-api/releases/latest">Download Now</a> • 
  <a href="https://github.com/ICME-Lab/kinic-api/wiki">Read Docs</a> • 
  <a href="https://github.com/ICME-Lab/kinic-api/issues">Get Help</a>
</p>