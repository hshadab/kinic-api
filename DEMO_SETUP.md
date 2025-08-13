# Multi-Agent Kinic Demo Setup Guide

## Two Ways to Run the Demo

### Option 1: Browser Mode (NO API Keys Needed) ✅ RECOMMENDED
This is the easiest and most visual way to demonstrate!

#### Setup:
1. Start Kinic API:
   ```powershell
   cd \\wsl.localhost\Ubuntu\home\hshadab\kinic
   python kinic-api.py
   ```

2. Open 3 browser tabs:
   - Tab 1: https://claude.ai
   - Tab 2: https://chat.openai.com
   - Tab 3: https://gemini.google.com

3. Run demo:
   ```powershell
   # In another PowerShell window
   cd \\wsl.localhost\Ubuntu\home\hshadab\kinic
   python demo-multi-agent-integrated.py --mode browser
   ```

#### What happens:
- The demo guides you through each step
- You manually paste prompts to each AI
- Kinic automatically saves the pages
- Shows semantic search in action
- Each AI appears to be "collaborating"

---

### Option 2: API Mode (Requires API Keys) 💰
Fully automated but costs money per run.

#### Setup API Keys:

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:GOOGLE_API_KEY = "AI..."
```

**Or pass directly:**
```powershell
python demo-multi-agent-integrated.py --mode api `
  --openai-key "sk-..." `
  --anthropic-key "sk-ant-..." `
  --google-key "AI..."
```

#### Install required libraries:
```bash
pip install openai anthropic google-generativeai
```

#### Costs per demo run:
- OpenAI GPT-4: ~$0.05
- Claude-3: ~$0.03
- Gemini Pro: ~$0.001
- **Total: ~$0.08 per demo**

---

## Demo Flow (3 Minutes)

### Minute 1: Knowledge Gathering
- **Claude**: Researches best sentiment models
- **GPT-4**: Finds implementation patterns
- **Gemini**: Studies deployment strategies
- Each saves 2-3 Hugging Face pages

### Minute 2: Semantic Search Magic
Show how searches find semantically related content:
- "model initialization" → finds "from_pretrained"
- "text processing" → finds "tokenization"
- "API deployment" → finds "FastAPI", "Gradio"

### Minute 3: Collaborative Building
- Agents use Kinic to build complete solution
- Show the final working code
- Demonstrate 20X speed improvement

---

## Quick Start Commands

### Simplest Demo (Browser Mode):
```powershell
# Terminal 1
python kinic-api.py

# Terminal 2
python demo-multi-agent-integrated.py
```

### Automated Demo (with APIs):
```powershell
# Terminal 1
python kinic-api.py

# Terminal 2 (with your API keys)
$env:OPENAI_API_KEY = "your-key"
$env:ANTHROPIC_API_KEY = "your-key"
$env:GOOGLE_API_KEY = "your-key"
python demo-multi-agent-integrated.py --mode api
```

---

## Talking Points During Demo

### When showing Browser Mode:
"Notice how each AI agent has a different role - Claude researches, GPT-4 implements, Gemini deploys. They're sharing knowledge through Kinic's semantic memory."

### During Semantic Search:
"Watch this - I search for 'model initialization' but Kinic finds pages about 'from_pretrained' and 'pipeline setup'. It understands MEANING, not just keywords."

### The Wow Moment:
"Traditional approach: 60 minutes reading docs. With Kinic: 3 minutes to working code. That's a 20X improvement."

### Closing:
"Kinic isn't just storage - it's shared consciousness for AI agents. Every page saved makes ALL agents smarter."

---

## Troubleshooting

**Issue**: "Kinic API not found"
**Fix**: Make sure `python kinic-api.py` is running

**Issue**: "Failed to save page"
**Fix**: Check Chrome is open with Kinic extension logged in

**Issue**: "No API keys found" (API mode)
**Fix**: Set environment variables or use --key arguments

**Issue**: Mouse clicks wrong position
**Fix**: Run `python fix-kinic-button.py` to recalibrate

---

## Demo Variations

### Variant 1: Debug Session
Instead of building an app, debug a real error using semantic search

### Variant 2: Cross-Language
Show Python, JavaScript, and Rust documentation connecting semantically

### Variant 3: Live Coding
Have agents actually write and run the code in real-time

---

## The Key Message

**"Three AI agents. Eight Hugging Face pages. One shared semantic memory.**
**Result: A complete sentiment API in 3 minutes.**

**Traditional search sees words.**
**Kinic sees connections.**

**This is the future of AI collaboration."**