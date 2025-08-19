# Google A2A + Kinic Integration Demo

## Overview
This demo shows how Google's A2A (Agent-to-Agent) protocol can be enhanced with Kinic's semantic memory for developer workflows.

**Demo Scenario**: Two developer agents (Code Reviewer + Security Specialist) collaborate to review a pull request with SQL injection vulnerability.

## Key Features
- **A2A Protocol Simulation**: Demonstrates agent-to-agent task routing
- **Kinic Semantic Memory**: Agents discover each other's knowledge automatically  
- **AI-Enhanced Analysis**: Uses Kinic's AI extraction for detailed security fixes
- **Real UI Automation**: Same proven automation as existing Kinic demos

## Architecture
```
Code Reviewer Agent ←─A2A Protocol─→ Security Specialist Agent
        ↓                                    ↓
   Kinic Semantic Memory ←─Discovery─→ Kinic Semantic Memory
        ↓                                    ↓
   Coding Standards                    Security Guidelines
   (PEP 8, Reviews)                   (OWASP, SQL Injection)
```

## Files
- `a2a-dev-demo.py` - Main demo implementation
- `requirements.txt` - Python dependencies
- `demo_config.json` - Demo configuration
- `README.md` - This file

## Prerequisites
- Kinic API running (`python ../kinic-api.py`)
- Chrome browser with Kinic extension
- Calibrated Kinic coordinates for your screen
- No Google APIs needed - this is a conceptual demonstration

## Usage
```bash
cd googlea2a
pip install -r requirements.txt
python a2a-dev-demo.py
```

## Demo Flow (5 minutes)
1. **Knowledge Capture** (2 min): Agents save documentation to Kinic
2. **A2A Handoff + Discovery** (1.5 min): Code issue → Security escalation  
3. **AI-Enhanced Fix** (1.5 min): Generate complete security solution

## Expected Results
- **Traditional Review**: 30+ minutes, manual security lookup
- **A2A + Kinic**: 5 minutes, AI-powered comprehensive fix
- **Security Issues Found**: 1 critical SQL injection with working code fix
- **Developer Experience**: Complete problem + solution + education