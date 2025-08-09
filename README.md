# Kinic API - Give Your AI Perfect Memory

**Save any webpage. Search with AI. Never lose information again.**

Transform your Kinic Chrome extension into a powerful memory system for AI assistants like Claude, ChatGPT, and Cursor.

## 🎯 What You Can Do

### Practical AI Memory Use Cases
- **🧠 Never Lose Research** - Save important articles, docs, and code snippets, then ask your AI to recall them anytime
- **💡 Context That Persists** - Your AI remembers everything from past sessions - no more re-explaining projects
- **🔍 Smart Code Search** - "What was that Python script I saved about webscraping?" - instant retrieval
- **📚 Personal Knowledge Base** - Build a searchable library of everything you've learned
- **🤝 Team Knowledge Sharing** - Share discoveries with your team through a common memory layer
- **🔄 Cross-Tool Memory** - Same memory works in VSCode, browser, terminal - everywhere

### Advanced Blockchain Features
> **🔗 Powered by on-chain vector database** - Your knowledge is verifiable, permanent, and truly yours
- **Proof of Learning** - Cryptographic evidence of what your AI learned from
- **Zero Vendor Lock-in** - No API fees, no service shutdowns, no data hostage
- **Censorship Resistant** - Your knowledge can't be deleted or restricted

## 🚀 Simple Setup (5 Minutes)

### Prerequisites
- Windows with Chrome browser
- [Kinic Chrome extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc) installed

### Step 1: Get the Code
Open PowerShell or Terminal and paste:
```bash
git clone https://github.com/hshadab/kinic-api.git
cd kinic-api
```

### Step 2: Install Python (if needed)
```bash
# Check if Python is installed
python --version

# If not installed, download from python.org
# Or on Windows: winget install Python.Python.3.12
```

### Step 3: Install Requirements
```bash
pip install flask flask-cors pyautogui pyperclip requests
```

### Step 4: Set Up Kinic Position
```bash
# This will count down from 10 - hover your mouse over the Kinic icon
python capture-position-10s.py

# Do the same for the AI response area in Kinic
python capture-ai-position.py
```

### Step 5: Start the API
```bash
python kinic-api.py
```

That's it! The API is now running at `http://localhost:5005`

## 📡 API Endpoints

Simple endpoints to control Kinic from your AI:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/save` | POST | Save current page to Kinic |
| `/search-and-retrieve` | POST | Search and get first URL |
| `/search-ai-extract` | POST | Search with AI analysis extraction |
| `/click` | POST | Open Kinic extension |
| `/close` | POST | Close Kinic extension |
| `/setup-kinic` | POST | Configure Kinic button position |
| `/setup-ai` | POST | Configure AI response position |

## 💬 How to Use with Your AI

### With Claude, ChatGPT, or Cursor
Just tell your AI:
```
"I have Kinic API running on localhost:5005. 
Save this webpage to my memory."

"Search my Kinic memory for that Python webscraping tutorial 
I saved last week and show me the code."
```

Your AI will handle the technical details!

### Quick Examples

**Save the current page:**
```python
import requests
requests.post('http://localhost:5005/save')
```

**Search and get URL:**
```python
result = requests.post('http://localhost:5005/search-and-retrieve', 
    json={'query': 'machine learning'})
print(result.json()['url'])
```

**Get AI analysis of saved content:**
```python
result = requests.post('http://localhost:5005/search-ai-extract', 
    json={'query': 'explain that Docker article I saved'})
print(result.json()['ai_response'])
```


## 🛠️ Troubleshooting

**"Python not found"**
- Download from [python.org](https://python.org) or use `winget install Python.Python.3.12`

**"Kinic button not clicking"**
- Re-run `python capture-position-10s.py` and make sure to hover over the Kinic icon

**"API not responding"**
- Make sure the server is running (you should see "Running on http://localhost:5005")
- Check that Chrome and Kinic extension are open

## 📋 Requirements

- Windows 10/11 (with WSL) or Linux/Mac
- Chrome browser with [Kinic extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc)
- Python 3.8 or newer

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs or request features via [Issues](https://github.com/hshadab/kinic-api/issues)
- Submit pull requests
- Share your use cases and integrations

## 📄 License

MIT License - Use it however you want!

## 🙏 About

Built to give AI agents perfect memory through Kinic's on-chain vector database. Your knowledge, your control, forever.