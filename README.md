# 🧠 Kinic - The AI Memory Layer for Multi-Agent Systems

<p align="center">
  <img src="brain-transparent-new.png" alt="Kinic Brain" width="200"/>
</p>

<p align="center">
  <strong>Build intelligent AI applications with persistent semantic memory</strong>
  <br>
  <a href="https://www.kinic.io">Get Started at kinic.io</a> • 
  <a href="#api-documentation">API Docs</a> • 
  <a href="#demos">Live Demos</a>
</p>

---

## What is Kinic?

Kinic is a revolutionary semantic memory platform that enables AI agents to store, retrieve, and share knowledge across sessions and applications. Think of it as a brain for your AI systems - a centralized memory layer that makes your agents truly intelligent and context-aware.

### 🚀 Create Your Free Account

**[Sign up at www.kinic.io](https://www.kinic.io)** to get your API key and start building with Kinic today. Your API key unlocks:

- ✅ **Unlimited memory storage** for your AI agents
- ✅ **Cross-session persistence** - agents remember everything
- ✅ **Multi-agent orchestration** - agents share knowledge seamlessly
- ✅ **Real-time sync** across all your applications
- ✅ **Enterprise-grade security** for your data

## Why Kinic?

### The Problem
Traditional AI agents are stateless - they forget everything between sessions. Building context-aware, intelligent applications requires complex infrastructure for memory management, retrieval, and synchronization.

### The Solution
Kinic provides a simple API that gives your AI agents perfect memory. Store anything, retrieve everything, and build applications that truly understand and remember your users.

## 🔥 Key Features

### Semantic Memory API
```python
# Store knowledge
kinic.store({
  "user_preference": "dark_mode",
  "context": "ui_settings",
  "metadata": {"timestamp": "2024-01-15"}
})

# Retrieve with natural language
memories = kinic.query("what UI preferences does the user have?")
```

### Multi-Agent Orchestration
Connect multiple AI agents (OpenAI, Anthropic, Perplexity) to a shared knowledge base. Agents can:
- Share discoveries and insights
- Collaborate on complex tasks
- Maintain context across conversations
- Build on each other's knowledge

### Real-Time Visualization
This repository includes a stunning visualization of your Kinic brain and connected agents. Watch knowledge flow in real-time as your agents interact with the memory layer.

## 🎥 See It In Action

### Two-Agent HuggingFace Demo
Watch how two AI agents collaborate using Kinic's memory layer to discover and share HuggingFace models:

**[📺 Watch the Demo Video](https://www.youtube.com/watch?v=Ooipwo4TGXY)**

In this simple yet powerful demonstration:
- **Agent 1** discovers and saves HuggingFace model information to Kinic
- **Agent 2** automatically finds and uses that knowledge through semantic search
- No direct communication needed - pure memory-based collaboration
- Real-world example of how Kinic enables AI teamwork

### Live Interactive Demos

| Demo | Description | Try It |
|------|-------------|--------|
| **Brain Visualization** | Watch your AI agents orbit around the Kinic memory core with real-time data flow | **[Launch →](https://hshadab.github.io/kinic-api/)** |
| **Google A2A Protocol** | See enterprise-grade agent-to-agent communication with memory persistence | **[Launch →](https://hshadab.github.io/kinic-api/demo-google-a2a-v2.html)** |
| **Agent Discovery** | Watch agents automatically discover and connect with each other | **[Launch →](https://hshadab.github.io/kinic-api/demo-2-agent-hf-discovery.html)** |

## 📦 What's in This Repository?

### 1. **🎮 AI Agent Control Center** 
Not just a visualization - a fully functional mission control for your AI agents:
- **Configure Tab**: Connect and authenticate AI agents (OpenAI, Anthropic, Perplexity)
- **Command Tab**: Send real-time commands to your agent network
- **Tasks Tab**: Set up automated workflows and background jobs
- **Live Metrics**: Monitor agent activity, connections, and memory usage
- **[Try it Live →](https://hshadab.github.io/kinic-api/)**

### 2. **🚀 Production-Ready Backend**
Working Flask API server with real AI platform integrations:
```python
# Just 4 lightweight dependencies!
flask==3.0.0
flask-cors==4.0.0
openai==1.12.0
anthropic==0.18.0
```
- Actual API connections (not mocked)
- Test endpoints for verification
- CORS-enabled for web apps
- Ready to deploy today

### 3. **🏢 Enterprise Ready**
- **Google A2A Protocol Support**: Works with industry-standard agent communication
- **[See A2A Demo →](https://hshadab.github.io/kinic-api/demo-google-a2a-v2.html)**
- **Multi-Platform**: OpenAI, Anthropic, Perplexity, and more
- **Secure**: API keys stored locally, never transmitted unnecessarily

### 4. **🧪 Developer Tools**
Complete testing and debugging infrastructure:
- **test-agent.html**: Standalone API connection tester
- **Health check endpoints**: Monitor system status
- **Real-time error reporting**: Clear feedback when things go wrong
- **Coordinate calibration tools**: For UI automation testing

## 💡 Simple Example: Two Agents Sharing Knowledge

Here's how easy it is for agents to collaborate through Kinic:

```python
# Agent 1: Researcher finds a great model
researcher = KinicAgent(api_key="your-kinic-key", role="researcher")
researcher.save("Found amazing sentiment model: cardiffnlp/twitter-roberta-base-sentiment")

# Agent 2: Builder (different session, different AI) needs a sentiment model
builder = KinicAgent(api_key="your-kinic-key", role="builder") 
models = builder.search("sentiment analysis models")
# Returns: "cardiffnlp/twitter-roberta-base-sentiment" - exactly what Agent 1 found!

# Builder uses the discovered model
builder.implement(f"Create API using {models[0]}")
```

That's it! No complex orchestration, no direct communication protocols. Just shared memory.

## ⚡ Why Developers Love Kinic

### Ridiculously Simple Setup
```bash
# Entire setup in 30 seconds
git clone https://github.com/hshadab/kinic-api.git
cd kinic-api
pip install -r requirements.txt  # Just 4 packages!
python kinic-agent-api.py        # You're live!
```

### Works With Your Existing Stack
- **Any AI Model**: OpenAI, Anthropic, Perplexity, HuggingFace, local models
- **Any Language**: Python client provided, REST API works with anything
- **Any Platform**: Web apps, CLI tools, notebooks, automation scripts
- **Any Scale**: From prototypes to production systems

### See Results Immediately
- Visual dashboard shows agent connections in real-time
- Test connections with actual API calls
- Monitor memory growth and agent collaboration
- Debug with clear error messages and health checks

## 🚀 Quick Start

### Step 1: Get Your API Key
**[Create your free account at www.kinic.io](https://www.kinic.io)** and grab your API key from the dashboard.

### Step 2: Clone This Repository
```bash
git clone https://github.com/hshadab/kinic-api.git
cd kinic-api
```

### Step 3: Set Up Your Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Your API Key
```python
# In your code
import os
os.environ['KINIC_API_KEY'] = 'your-api-key-from-kinic.io'
```

### Step 5: Run the Demo
```bash
# Start the agent backend
python kinic-agent-api.py

# Open the visualization in your browser
open index.html
```

## API Documentation

### Core Endpoints
All API requests require your Kinic API key from [www.kinic.io](https://www.kinic.io).

```python
# Initialize client
from kinic import KinicClient
client = KinicClient(api_key="your-key-from-kinic.io")

# Store memory
client.store_memory(
    content="User prefers Python for data science tasks",
    category="user_preferences",
    tags=["python", "data_science", "preferences"]
)

# Query memories
results = client.query_memories(
    query="What programming languages does the user know?",
    limit=10
)

# Delete specific memory
client.delete_memory(memory_id="mem_123")
```

### Agent Integration

Connect your favorite AI models to Kinic:

```python
# Connect OpenAI with Kinic memory
from kinic import KinicAgent

agent = KinicAgent(
    kinic_api_key="your-kinic-key",
    openai_api_key="your-openai-key",
    model="gpt-4"
)

# Agent automatically uses Kinic for memory
response = agent.chat("Remember that I prefer Python for ML tasks")
# This preference is now stored in Kinic

# Later, even in a new session
response = agent.chat("What's my preferred language for ML?")
# Returns: "You prefer Python for ML tasks"
```

## 🎨 Visualization Features

The included brain visualization showcases:

- **3D Neural Network** - Your Kinic brain pulsing with activity
- **Agent Constellation** - AI agents orbiting your knowledge core
- **Data Flow Particles** - Watch memories being stored and retrieved
- **Real-time Metrics** - Monitor connections, storage, and activity
- **Configuration Panel** - Set up and test agent connections
- **Command Interface** - Direct control over your AI ecosystem

## 🛠 Advanced Usage

### Multi-Agent Workflows

```python
# Create specialized agents sharing one Kinic brain
researcher = KinicAgent(role="researcher", model="gpt-4")
analyst = KinicAgent(role="analyst", model="claude-3")
builder = KinicAgent(role="builder", model="gpt-4")

# Researcher discovers information
researcher.process("Find the latest ML optimization techniques")

# Analyst can access researcher's findings
analyst.process("Analyze the techniques found and rank by efficiency")

# Builder uses both agents' knowledge
builder.process("Implement the top-ranked optimization technique")
```

### Semantic Search

```python
# Store rich, contextual information
client.store_memory({
    "content": "Customer prefers email communication on Tuesdays",
    "embedding": generate_embedding(content),
    "metadata": {
        "customer_id": "cust_123",
        "preference_type": "communication",
        "confidence": 0.95
    }
})

# Semantic similarity search
similar_memories = client.search_similar(
    query_embedding=generate_embedding("communication preferences"),
    threshold=0.8
)
```

## 🌟 Use Cases

### Personal AI Assistant
Build an AI that truly knows you - your preferences, history, and context persist forever.

### Customer Support
Agents that remember every interaction, preference, and issue across all channels.

### Research & Development
Multiple AI agents collaborating on complex problems, building on shared discoveries.

### Content Creation
AI systems that maintain consistency in tone, style, and narrative across projects.

### Education
Tutoring systems that adapt to each student's learning pattern and progress.

## 🤝 Community & Support

- **Documentation**: Full API docs available after login at [www.kinic.io](https://www.kinic.io)
- **Discord**: Join our community for support and updates
- **GitHub Issues**: Report bugs or request features
- **Enterprise**: Contact us for dedicated support and custom solutions

## 🚦 Getting Started Checklist

- [ ] **[Sign up at www.kinic.io](https://www.kinic.io)** for your free account
- [ ] Get your API key from the dashboard
- [ ] Clone this repository
- [ ] Run the visualization demo
- [ ] Connect your first AI agent
- [ ] Store your first memory
- [ ] Build something amazing!

## 📄 License

This repository is provided for use with the Kinic platform. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Ready to give your AI perfect memory?</strong>
  <br><br>
  <a href="https://www.kinic.io">
    <img src="https://img.shields.io/badge/Get%20Started-kinic.io-00ff88?style=for-the-badge&labelColor=0a0e27" alt="Get Started at kinic.io"/>
  </a>
</p>

<p align="center">
  <sub>Built with ❤️ by the Kinic team</sub>
</p>