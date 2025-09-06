#!/usr/bin/env python3
"""
A2A + Kinic Demo: Intelligent Code Review System
=================================================
Shows how A2A protocol handles agent communication while Kinic provides semantic memory.

UNIQUE CAPABILITIES DEMONSTRATED:
1. Agents discover each other by expertise, not hardcoded names
2. Knowledge accumulates - each review makes future reviews smarter
3. Cross-vendor agents (OpenAI, Anthropic) collaborate via standard protocol
4. Semantic routing - finds the RIGHT expert for each issue type
"""

import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Simulated A2A Protocol Handler
@dataclass
class A2AMessage:
    """Google A2A Protocol Message Format"""
    id: str
    method: str
    params: Dict
    from_agent: str
    to_agent: Optional[str] = None
    timestamp: Optional[str] = None

class A2AProtocol:
    """Simulates Google A2A Protocol for agent communication"""
    
    def __init__(self):
        self.registered_agents = {}
        self.message_log = []
    
    def register_agent(self, agent_id: str, capabilities: List[str], endpoint: str):
        """Register an agent with its capabilities"""
        self.registered_agents[agent_id] = {
            "capabilities": capabilities,
            "endpoint": endpoint,
            "status": "available"
        }
        print(f"✅ A2A: Registered {agent_id} with capabilities: {capabilities}")
    
    def send_message(self, message: A2AMessage):
        """Send message via A2A protocol"""
        message.timestamp = datetime.now().isoformat()
        self.message_log.append(message)
        print(f"📤 A2A Message: {message.from_agent} → {message.to_agent or 'broadcast'}")
        print(f"   Method: {message.method}")
        return {"status": "delivered", "message_id": message.id}
    
    def discover_agents(self, capability_query: str = None):
        """Discover available agents"""
        if capability_query:
            return {
                agent_id: info 
                for agent_id, info in self.registered_agents.items()
                if any(capability_query.lower() in cap.lower() 
                      for cap in info["capabilities"])
            }
        return self.registered_agents

# Simulated Kinic Semantic Memory
class KinicMemory:
    """Simulates Kinic's semantic memory and search capabilities"""
    
    def __init__(self):
        self.memories = []
        self.expertise_graph = {}
    
    def store(self, content: str, metadata: Dict):
        """Store knowledge in Kinic"""
        memory = {
            "id": f"mem_{len(self.memories)}",
            "content": content,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        self.memories.append(memory)
        
        # Build expertise graph
        agent = metadata.get("agent")
        issue_type = metadata.get("issue_type")
        if agent and issue_type:
            if agent not in self.expertise_graph:
                self.expertise_graph[agent] = {}
            if issue_type not in self.expertise_graph[agent]:
                self.expertise_graph[agent][issue_type] = {"count": 0, "success_rate": 0}
            self.expertise_graph[agent][issue_type]["count"] += 1
        
        print(f"💾 Kinic: Stored memory about {metadata.get('issue_type', 'general')}")
        return memory["id"]
    
    def semantic_search(self, query: str, limit: int = 5):
        """Semantic search through memories"""
        # Simplified semantic matching
        results = []
        for memory in self.memories:
            if query.lower() in memory["content"].lower():
                results.append(memory)
        
        print(f"🔍 Kinic: Found {len(results)} relevant memories for '{query}'")
        return results[:limit]
    
    def find_expert(self, issue_type: str):
        """Find the best agent for a specific issue type"""
        best_agent = None
        best_score = 0
        
        for agent, expertise in self.expertise_graph.items():
            for known_issue, stats in expertise.items():
                # Semantic similarity (simplified)
                if issue_type.lower() in known_issue.lower() or known_issue.lower() in issue_type.lower():
                    score = stats["count"] * (stats.get("success_rate", 0.5) + 0.5)
                    if score > best_score:
                        best_score = score
                        best_agent = agent
        
        if best_agent:
            print(f"🎯 Kinic: Best expert for '{issue_type}' is {best_agent} (score: {best_score:.2f})")
        return best_agent

# Agent Implementation
class CodeReviewAgent:
    """An agent that can review code"""
    
    def __init__(self, agent_id: str, model: str, specialties: List[str], 
                 a2a: A2AProtocol, kinic: KinicMemory):
        self.agent_id = agent_id
        self.model = model
        self.specialties = specialties
        self.a2a = a2a
        self.kinic = kinic
        
        # Register with A2A
        self.a2a.register_agent(
            agent_id=self.agent_id,
            capabilities=self.specialties,
            endpoint=f"agent://{agent_id}/v1"
        )
    
    def review_code(self, code: str, issue_type: str):
        """Review code and store insights in Kinic"""
        print(f"\n🤖 {self.agent_id} ({self.model}) reviewing for: {issue_type}")
        
        # Check Kinic for similar past issues
        past_issues = self.kinic.semantic_search(issue_type, limit=3)
        if past_issues:
            print(f"   📚 Found {len(past_issues)} similar past reviews to learn from")
        
        # Simulate review
        time.sleep(1)  # Simulate processing
        
        review_result = {
            "agent": self.agent_id,
            "issue_type": issue_type,
            "findings": f"Found issues related to {issue_type}",
            "recommendation": f"Fix {issue_type} by applying best practices",
            "learned_from_past": len(past_issues) > 0
        }
        
        # Store knowledge in Kinic
        self.kinic.store(
            content=f"Review of {issue_type}: {review_result['recommendation']}",
            metadata={
                "agent": self.agent_id,
                "issue_type": issue_type,
                "success": True
            }
        )
        
        return review_result

# DEMO: Intelligent Code Review System
def demo_code_review_system():
    """
    Demonstrates A2A + Kinic working together for intelligent code reviews.
    Each review makes the system smarter through accumulated knowledge.
    """
    print("=" * 70)
    print("DEMO: A2A + Kinic Intelligent Code Review System")
    print("=" * 70)
    
    # Initialize systems
    a2a = A2AProtocol()
    kinic = KinicMemory()
    
    # Create diverse agents from different vendors
    agents = [
        CodeReviewAgent(
            agent_id="security-expert",
            model="claude-3-opus",  # Anthropic
            specialties=["SQL injection", "XSS attacks", "authentication"],
            a2a=a2a,
            kinic=kinic
        ),
        CodeReviewAgent(
            agent_id="performance-optimizer", 
            model="gpt-4-turbo",  # OpenAI
            specialties=["database optimization", "caching", "async patterns"],
            a2a=a2a,
            kinic=kinic
        ),
        CodeReviewAgent(
            agent_id="react-specialist",
            model="gpt-4",  # OpenAI
            specialties=["React hooks", "state management", "component optimization"],
            a2a=a2a,
            kinic=kinic
        ),
        CodeReviewAgent(
            agent_id="python-expert",
            model="claude-3-sonnet",  # Anthropic  
            specialties=["Python patterns", "type hints", "PEP compliance"],
            a2a=a2a,
            kinic=kinic
        )
    ]
    
    # Simulate incoming PRs with different issues
    pull_requests = [
        {"code": "SELECT * FROM users WHERE name = '" + "'", "issues": ["SQL injection vulnerability"]},
        {"code": "const [data, setData] = useState()", "issues": ["React hooks usage"]},
        {"code": "def process(x): return x", "issues": ["Python patterns", "type hints missing"]},
        {"code": "SELECT * FROM orders", "issues": ["database optimization needed"]},
        {"code": "user_input = request.form['data']", "issues": ["XSS attacks possible"]},
    ]
    
    print("\n📋 Processing Pull Requests...")
    print("-" * 50)
    
    for i, pr in enumerate(pull_requests, 1):
        print(f"\n🔄 PR #{i}: Issues detected: {pr['issues']}")
        
        for issue in pr["issues"]:
            # UNIQUE CAPABILITY 1: Semantic discovery of expert
            # Not hardcoded - Kinic finds the best agent based on past performance
            expert = kinic.find_expert(issue)
            
            if not expert:
                # No expert found in history, use A2A discovery
                print(f"   🔎 No expert history, using A2A discovery for '{issue}'")
                discovered = a2a.discover_agents(issue)
                if discovered:
                    expert = list(discovered.keys())[0]
                    print(f"   ✨ A2A discovered: {expert}")
            
            if expert:
                # Find the agent object
                agent = next((a for a in agents if a.agent_id == expert), None)
                if agent:
                    # A2A handles the communication protocol
                    message = A2AMessage(
                        id=f"review_{i}_{issue.replace(' ', '_')}",
                        method="review_code",
                        params={"code": pr["code"], "issue_type": issue},
                        from_agent="orchestrator",
                        to_agent=expert
                    )
                    a2a.send_message(message)
                    
                    # Agent performs review
                    result = agent.review_code(pr["code"], issue)
                    
                    # UNIQUE CAPABILITY 2: Knowledge accumulates
                    print(f"   ✅ Review complete. System is now smarter about {issue}")
    
    # Show accumulated expertise
    print("\n" + "=" * 70)
    print("📊 ACCUMULATED EXPERTISE GRAPH (Kinic Knowledge)")
    print("-" * 50)
    for agent, expertise in kinic.expertise_graph.items():
        print(f"\n🤖 {agent}:")
        for issue_type, stats in expertise.items():
            print(f"   • {issue_type}: {stats['count']} reviews")
    
    # Demonstrate improved routing
    print("\n" + "=" * 70)
    print("🎯 DEMONSTRATION: System Has Learned Expert Routing")
    print("-" * 50)
    
    test_issues = ["SQL injection in API", "React performance issue", "Python code style"]
    for issue in test_issues:
        expert = kinic.find_expert(issue)
        if expert:
            print(f"✨ '{issue}' → Routes to: {expert}")
        else:
            print(f"🔍 '{issue}' → Would use A2A discovery")
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete: A2A handled protocol, Kinic provided intelligence")
    print("=" * 70)

# Run the demo
if __name__ == "__main__":
    demo_code_review_system()