# Kinic API - On-Chain Vector Database for AI Agents

Transform your Kinic Chrome extension into a powerful API for LLM copilots and AI agents.

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

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/hshadab/kinic-api.git
cd kinic-api
pip install flask flask-cors pyautogui pyperclip requests
```

### Setup Coordinates
```bash
# Capture Kinic button position (10-second timer)
python3 capture-position-10s.py

# Capture AI response area position
python3 capture-ai-position.py
```

### Run the API Server
```bash
python3 kinic-api-v5.py
```

The API runs on `http://localhost:5005`

## ✨ Features

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
| `/search-and-retrieve` | POST | Search and get first URL |
| `/search-ai-extract` | POST | Search with AI analysis extraction |
| `/click` | POST | Open Kinic extension |
| `/close` | POST | Close Kinic extension |
| `/setup-kinic` | POST | Configure Kinic button position |
| `/setup-ai` | POST | Configure AI response position |

## 🛠️ Integration Examples

### LLM Copilot (Claude, ChatGPT, etc.)
Tell your AI assistant:
```
"I have a Kinic API running on localhost:5005. 
Save this page to my Kinic memory: [current URL]"

"Search my Kinic for information about quantum computing 
and extract the AI analysis"
```

### Python Script
```python
import requests

# Save current browser page
requests.post('http://localhost:5005/save')

# Search and get URL
result = requests.post('http://localhost:5005/search-and-retrieve', 
    json={'query': 'machine learning'})
print(result.json()['url'])

# Search and extract AI analysis
result = requests.post('http://localhost:5005/search-ai-extract', 
    json={'query': 'explain transformers'})
print(result.json()['ai_response'])
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


## 📋 Requirements

- Windows 10/11 with WSL or native Linux
- Chrome browser with [Kinic extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc)
- Python 3.8+

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs or request features via [Issues](https://github.com/hshadab/kinic-api/issues)
- Submit pull requests
- Share your integration examples

## 📄 License

MIT License

## 🙏 Acknowledgments

Built for the Kinic community to enable powerful AI agent integrations with on-chain memory.