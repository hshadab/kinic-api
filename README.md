# Kinic Automation Suite

Transform your Kinic Chrome extension into a powerful API with desktop app - no coding required!

## 🚀 Quick Start - Download Desktop App

Get started in 30 seconds with our user-friendly desktop application:

### Download Latest Build:
[![Download for Windows](https://img.shields.io/badge/Download-Windows-blue?style=for-the-badge&logo=windows)](https://github.com/ICME-Lab/kinic/actions/workflows/build-desktop.yml)
[![Download for macOS](https://img.shields.io/badge/Download-macOS-black?style=for-the-badge&logo=apple)](https://github.com/ICME-Lab/kinic/actions/workflows/build-desktop.yml)

> **Note:** Click the links above, then select the latest workflow run and download the artifact for your platform from the "Artifacts" section (requires GitHub login)

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

### API Endpoints
Transform Kinic into a powerful API for your workflows:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/save` | POST | Save current page to Kinic |
| `/api/search` | POST | Search your Kinic memory |
| `/api/search-ai` | POST | Search with AI analysis |
| `/api/ai` | POST | Trigger AI assistance |

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
curl -X POST http://localhost:5000/api/save

# Search with AI
curl -X POST http://localhost:5000/api/search-ai \
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