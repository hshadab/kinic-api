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

## 🧠 Why Vector Database Memory Changes Everything

### The Fundamental Difference

**Traditional Storage (Supabase, Google Drive, Databases):**
- Stores data as files or records
- Keyword search only
- You manually organize everything
- No understanding of meaning or relationships
- Each search starts from zero

**Kinic's Vector Database:**
- Converts content into high-dimensional vectors (embeddings)
- **Understands meaning**, not just keywords
- Automatically builds knowledge graphs
- Finds semantic relationships you didn't know existed
- Every piece of information makes the entire system smarter

### Real Example from Our Demo

When Agent 3 asks *"explain how to implement Stripe payments with best practices"*:

**Kinic's Vector Search Returns:**
- Synthesized knowledge from ALL saved Stripe docs
- Related implementation patterns from different sources
- Security considerations you saved weeks ago
- 438+ characters of contextual insights
- Connections between payment flows and error handling you never explicitly linked

**Traditional Database Would Need:**
```python
# Manual queries for each piece
SELECT * FROM docs WHERE title LIKE '%stripe%'
SELECT * FROM docs WHERE title LIKE '%payment%'
SELECT * FROM docs WHERE title LIKE '%checkout%'
# Hope you didn't miss anything...
# Manually piece together the results
```

### The Killer Feature: Semantic Understanding

```python
# You search for: "authentication problems"

# Kinic finds:
- OAuth flow documentation
- JWT token expiration issues
- Session management bugs
- CORS errors (because they often relate to auth)
- Rate limiting (commonly affects auth endpoints)
- That Stack Overflow about refresh tokens

# Even though NONE of these contained the word "authentication problems"
```

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
                                              ▼
                                    Semantic Understanding
                                    Knowledge Synthesis
                                    Automatic Relationships
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

### What Makes This Demo Special

The three agents demonstrate how Kinic's vector database enables true knowledge synthesis:

1. **Agent 1** saves multiple Stripe documentation pages
2. **Agent 2** searches for "stripe checkout" and retrieves the exact URL
3. **Agent 3** asks for implementation best practices and receives 438+ characters of AI-synthesized insights

The agents never communicate directly - they're accessing the same blockchain-based vector memory. Every piece of saved information makes ALL future queries smarter.

## 💼 Real-World Workflow Examples

### Debugging Production Issues
**Without Kinic:** Search Slack, Google Drive, GitHub, Notion, browser bookmarks separately. Manually piece together solution. *Time: 45+ minutes*

**With Kinic:**
```python
"Our app is throwing 500 errors, what have we learned about this?"
# Returns: Redis timeout discussions, architecture docs, Stack Overflow solutions,
# runbooks, similar patterns - all synthesized. Time: 30 seconds
```

### Code Review Intelligence
**Without Kinic:** Manually remember all best practices, previous PR comments, security guidelines

**With Kinic:**
```python
"Review this auth code against our patterns and security standards"
# Returns: "JWT expiration inconsistent with PR #234, missing rate limiting 
# from security audit, violates OWASP guideline we saved last month"
```

### Onboarding New Developers
**Without Kinic:** "Docs are in Confluence, Drive, Notion, GitHub wikis, and that Slack thread..."

**With Kinic:**
```python
"I'm new to the payment service, explain our implementation"
# Returns: Synthesized knowledge from ALL sources - architecture decisions,
# bug fixes, optimizations, security considerations - as cohesive documentation
```

### Learning & Implementation
**Traditional:** Save tutorial Monday, lose it by Wednesday, start over Friday

**With Kinic:**
```python
# Monday: "Save this WebSocket tutorial"
# Wednesday: "Show me WebSocket examples" 
# Friday: "How do we handle disconnections in our WebSocket implementation?"
# Returns: Synthesized best practices from ALL saved content with your team's specific patterns
```

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

## 🎯 The Kinic Difference

### Traditional Knowledge Management
- ❌ You organize the information
- ❌ You create the connections  
- ❌ You remember where things are
- ❌ You hope you tagged correctly
- ❌ Knowledge degrades over time
- ❌ Each search starts from zero

### Kinic Vector Intelligence
- ✅ Information organizes itself
- ✅ Connections emerge automatically
- ✅ AI understands context and meaning
- ✅ Discovery happens naturally
- ✅ Knowledge compounds over time
- ✅ Every query gets smarter

**The Bottom Line:** With traditional storage, you're managing files. With Kinic, you're building collective intelligence that grows with every use.

## 🙏 About

Built to give AI agents perfect memory through Kinic's on-chain vector database. Your knowledge, your control, forever.

Every Fortune 500 is racing to give their AI agents memory. This project proves you can do it today with just a Chrome extension.

**The future isn't AI with better prompts. It's AI that actually remembers.**

---

**Recent Updates (v2.0)**
- ✅ Fixed WSL coordinate translation issues
- ✅ Standardized all endpoints with 5-step pattern
- ✅ Extended save timeout to 8 seconds
- ✅ Added visual marketing demo
- ✅ AI extraction verified: 438+ characters
- ✅ Multi-agent collaboration demonstrated