# Multi-Agent Demos with Kinic

Demonstrate the power of shared memory across multiple AI agents!

## 🎯 Why Multi-Agent Systems?

With Kinic, multiple agents can:
- **Share Knowledge** - One agent's discoveries become available to all
- **Specialize** - Each agent focuses on what it does best
- **Collaborate** - Build on each other's work without direct communication
- **Scale** - Add more agents without changing the architecture

## 🚀 Quick Start

### 1. Simple Demo (2 Agents)
Perfect for beginners - shows basic knowledge sharing:

```bash
python simple-multi-agent.py
```

**What it does:**
- Agent 1: Saves code to Kinic
- Agent 2: Reviews the code from shared memory

### 2. Advanced Demo (3 Agents)
Full research team collaboration:

```bash
python multi-agent-demo.py
```

**What it does:**
- ResearchBot: Collects articles
- AnalysisBot: Analyzes content
- SummaryBot: Creates final report

## 💡 Demo Ideas to Try

### Customer Support Team
```python
# Agent 1: Saves customer questions
# Agent 2: Searches for similar past issues
# Agent 3: Generates solutions from history
```

### Learning Assistant Network
```python
# Agent 1: Saves learning materials
# Agent 2: Creates practice questions
# Agent 3: Tracks progress and suggests next topics
```

### Code Development Pipeline
```python
# Agent 1: Saves code snippets and documentation
# Agent 2: Generates tests
# Agent 3: Reviews for security issues
# Agent 4: Suggests optimizations
```

## 🔧 Building Your Own Multi-Agent System

### Basic Pattern
```python
import requests

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.api = "http://localhost:5005"
    
    def save_knowledge(self):
        requests.post(f"{self.api}/save")
    
    def use_shared_knowledge(self, query):
        return requests.post(
            f"{self.api}/search-ai-extract",
            json={"query": query}
        )

# Create specialized agents
researcher = Agent("Researcher", "Find information")
analyzer = Agent("Analyzer", "Process data")
writer = Agent("Writer", "Create reports")
```

## 🎮 Interactive Multi-Agent Playground

Want to see agents interact in real-time? Try this:

1. Open 3 terminal windows
2. Run a different agent script in each
3. Watch them share discoveries through Kinic!

```bash
# Terminal 1
python agent-researcher.py

# Terminal 2  
python agent-analyzer.py

# Terminal 3
python agent-writer.py
```

## 🌟 Advanced Patterns

### Agent Handoff
One agent completes a task and signals the next:
```python
# Agent 1 saves and tags content
save_with_tag("research_complete")

# Agent 2 waits for tag
wait_for_tag("research_complete")
analyze_content()
```

### Voting System
Multiple agents vote on decisions:
```python
# Each agent saves their analysis
agent1.save_opinion("approach_a: good")
agent2.save_opinion("approach_b: better")
agent3.save_opinion("approach_a: good")

# Aggregator counts votes
decide_by_majority()
```

### Specialist Network
Agents with different expertise:
```python
python_expert = Agent("PythonBot", "Python code")
js_expert = Agent("JSBot", "JavaScript code")
sql_expert = Agent("SQLBot", "Database queries")

# Route questions to right expert
route_to_specialist(question)
```

## 📊 Visualizing Agent Collaboration

Run the visualization script to see agents in action:
```bash
python visualize-agents.py
```

This shows:
- Active agents
- Knowledge flow between agents
- Memory growth over time
- Query patterns

## 🚦 Best Practices

1. **Clear Roles** - Each agent should have a specific purpose
2. **Tag Content** - Use descriptive searches to find specific knowledge
3. **Throttle Requests** - Add delays between API calls
4. **Error Handling** - Agents should gracefully handle failures
5. **Logging** - Track what each agent does for debugging

## 🎯 Challenge Yourself

Try building these multi-agent systems:

### Beginner
- Two agents playing 20 questions using shared memory

### Intermediate  
- Research team for any Wikipedia topic
- Code documentation generator pipeline

### Advanced
- Autonomous blog writing system
- Multi-agent debugging assistant
- Competitive agents trying to solve puzzles

## 📈 Scaling Up

The same patterns work with:
- 10 agents
- 100 agents
- 1000 agents

All sharing the same Kinic memory!

## 🤝 Share Your Creations

Built something cool? Share it!
- Add your demo to this repo
- Tweet with #KinicAgents
- Join the discussion at kinic.io

---

**Remember:** Every agent that uses Kinic makes the shared memory more valuable for all other agents. This is the power of collective intelligence!