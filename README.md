# Kinic API - AI Memory on Blockchain

**Control the Kinic Chrome Extension programmatically to give your AI agents persistent memory on the blockchain.**

Transform your Kinic Chrome extension into a powerful memory system for AI assistants like Claude, ChatGPT, and Cursor.

## 📖 What is Kinic?

Kinic is a Chrome extension that lets you save and search any webpage using AI. It stores your knowledge in an on-chain vector database, making it permanent and searchable forever. The Kinic API provides programmatic control over the extension, enabling AI agents to have persistent, blockchain-based memory.

**First time using Kinic?** 
👉 **[Get your free account at kinic.io](https://kinic.io)** and install the Chrome extension

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

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   AI Agent  │────▶│  Kinic API   │────▶│ Kinic Extension │
│  (Python)   │     │  (Flask)     │     │   (Chrome)      │
└─────────────┘     └──────────────┘     └─────────────────┘
                            │                      │
                            ▼                      ▼
                      PyAutoGUI            Blockchain Storage
                    (Mouse/Keyboard)        (Vector Database)
```

## 🚀 Quick Setup (Windows)

### Prerequisites
1. **Kinic Account** - [Sign up free at kinic.io](https://kinic.io)
2. **Chrome Browser** with [Kinic extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc) installed
3. **Windows 10/11** with Python 3.8+

### Step 1: Get the Code
Open PowerShell and run:
```powershell
git clone https://github.com/hshadab/kinic.git
cd kinic
```

### Step 2: Install Python (if needed)
```powershell
# Check if Python is installed
python --version

# If not installed, use winget:
winget install Python.Python.3.12
```

### Step 3: Install Requirements
```powershell
pip install flask flask-cors pyautogui pyperclip requests
```

### Step 4: Capture Kinic Button Position
```powershell
python capture-mouse-windows.py
```
Position your mouse over the Kinic extension icon when prompted and wait for countdown.

### Step 5: Capture AI Response Position
```powershell
python capture-ai-windows.py
```
1. Open Kinic and do a search
2. Click the AI button
3. When AI text appears, position mouse in CENTER of text
4. Press Enter to capture

### Step 6: Start the API
```powershell
python kinic-api.py
```

That's it! The API is now running at `http://localhost:5006`

## ✅ Test AI Extraction

```powershell
python test-ai-extraction-simple.py
```

You should see the AI-generated text extracted successfully!

## 📡 API Endpoints

All main endpoints follow a consistent pattern:
1. **Focus Chrome** (click safe area)
2. **Close existing popup** (ESC key)
3. **Open Kinic** at configured position
4. **Perform action** (save/search/extract)
5. **Close Kinic** (ESC key)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status and configuration |
| `/save` | POST | Save current page to Kinic (uses SHIFT+TAB) |
| `/search-and-retrieve` | POST | Search and get first URL |
| `/search-ai-extract` | POST | Search with AI analysis extraction |
| `/click` | POST | Open Kinic extension |
| `/close` | POST | Close Kinic extension |
| `/setup-kinic` | POST | Update Kinic button position |
| `/setup-ai` | POST | Update AI response position |

## 💬 How to Use with Your AI

### With Claude, ChatGPT, or Cursor
Just tell your AI:
```
"I have Kinic API running on localhost:5006. 
Save this webpage to my memory."

"Search my Kinic memory for that Python webscraping tutorial 
I saved last week and show me the code."
```

Your AI will handle the technical details!

### Quick Examples

**Save the current page:**
```python
import requests
requests.post('http://localhost:5006/save')
```

**Search and get URL:**
```python
result = requests.post('http://localhost:5006/search-and-retrieve', 
    json={'query': 'machine learning'})
print(result.json()['url'])
```

**Get AI analysis of saved content:**
```python
result = requests.post('http://localhost:5006/search-ai-extract', 
    json={'query': 'explain that Docker article I saved'})
print(result.json()['ai_response'])
# Returns actual AI-generated insights about your saved content!
```

## 🎭 Visual Demo

See the multi-agent collaboration in action:

```powershell
python stripe-demo-visual.py
```

This demo showcases:
- **3 AI Agents** working together through shared blockchain memory
- **Live visualization** of inputs and outputs
- **Real-time progress** tracking
- **No direct communication** between agents - only through Kinic

## 🛠️ Troubleshooting

### Coordinate Issues

**"Kinic button not clicking correctly"**
```powershell
python fix-kinic-button.py
```

**"AI text not being extracted"**
```powershell
python fix-ai-position.py
```

### Common Problems

**"Python not found"**
- Install Python: `winget install Python.Python.3.12`

**"Mouse position keeps changing"**
- Ensure Chrome window is maximized consistently
- Re-run the fix scripts when resolution changes

**"AI extraction returning empty"**
- Make sure to position mouse in CENTER of AI text when capturing
- Wait for AI text to fully generate (10+ seconds)

**"Running from WSL?"**
- Use PowerShell instead - WSL has coordinate translation issues
- The API now uses native Windows PyAutoGUI to avoid WSL problems

## 📋 Files Overview

### Core Files
- `kinic-api.py` - Main API server with standardized endpoints
- `kinic-config.json` - Stores coordinate configuration

### Setup & Calibration
- `capture-mouse-windows.py` - Initial Kinic button setup
- `capture-ai-windows.py` - Initial AI response area setup
- `fix-kinic-button.py` - Quick recalibration for Kinic button
- `fix-ai-position.py` - Quick recalibration for AI area

### Demo & Testing
- `stripe-demo-visual.py` - Visual multi-agent collaboration demo
- `test-ai-extraction-simple.py` - Test AI text extraction
- `test-mouse-movement.py` - Test mouse positioning

## 🔧 Technical Details

### Standardized Action Pattern
All endpoints follow a reliable 5-step sequence:
1. **Focus Chrome** - Click safe area (500, 500)
2. **Close popup** - ESC key (clears any existing state)
3. **Open Kinic** - Click at configured position
4. **Perform action** - Save/Search/Extract
5. **Close Kinic** - ESC key

### Timing Configuration
- **Kinic open**: 3 seconds
- **Search results**: 4 seconds
- **AI generation**: 10 seconds
- **Page save**: 8 seconds (full content)
- **Triple-click**: 20ms intervals

### Current Working Coordinates
```json
{
    "kinic_x": 2088,
    "kinic_y": 148,
    "ai_response_x": 1438,
    "ai_response_y": 1259
}
```

## 📋 Requirements

- Windows 10/11 (or WSL with display)
- Chrome browser with [Kinic extension](https://chrome.google.com/webstore/detail/kinic/mnddmednohmjdgmpbaieolebflkbcbjc)
- Python 3.8 or newer
- Required packages: flask, flask-cors, pyautogui, pyperclip, requests

## 🤝 Contributing

We welcome contributions! Feel free to:
- Report bugs or request features via [Issues](https://github.com/hshadab/kinic/issues)
- Submit pull requests
- Share your use cases and integrations

## 📄 License

MIT License - Use it however you want!

## 🙏 About

Built to give AI agents perfect memory through Kinic's on-chain vector database. Your knowledge, your control, forever.

---

**Recent Updates (v2.0)**
- ✅ Fixed WSL coordinate translation issues
- ✅ Standardized all endpoints with 5-step pattern
- ✅ Extended save timeout to 8 seconds
- ✅ Added visual marketing demo
- ✅ AI extraction verified: 438+ characters