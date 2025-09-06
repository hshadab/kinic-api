#!/usr/bin/env python3
"""
A2A + Kinic Demo: Multi-Vendor Agent Marketplace
================================================
Shows how agents from different AI vendors can discover and hire each other.

UNIQUE CAPABILITIES:
1. Cross-vendor discovery (OpenAI agents find Anthropic agents)
2. Reputation system based on actual performance
3. Cost optimization through intelligent routing
4. Skills marketplace with semantic matching
"""

import json
import random
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass 
class AgentListing:
    """Marketplace listing for an agent"""
    agent_id: str
    vendor: str
    model: str
    skills: List[str]
    cost_per_task: float
    rating: float = 5.0
    completed_tasks: int = 0
    availability: str = "available"

class A2AMarketplace:
    """A2A Protocol-based marketplace for agent discovery"""
    
    def __init__(self):
        self.listings = {}
        self.transactions = []
    
    def list_agent(self, listing: AgentListing):
        """List an agent on the marketplace"""
        self.listings[listing.agent_id] = listing
        print(f"📢 A2A Marketplace: {listing.vendor}'s {listing.agent_id} listed")
        print(f"   Skills: {', '.join(listing.skills[:3])}...")
        print(f"   Cost: ${listing.cost_per_task:.2f}/task")
    
    def discover_by_skill(self, skill_needed: str, max_cost: float = None):
        """Discover agents by skill requirement"""
        matches = []
        for agent_id, listing in self.listings.items():
            # Semantic skill matching (simplified)
            for skill in listing.skills:
                if skill_needed.lower() in skill.lower() or skill.lower() in skill_needed.lower():
                    if max_cost is None or listing.cost_per_task <= max_cost:
                        matches.append(listing)
                        break
        
        # Sort by rating and cost
        matches.sort(key=lambda x: (-x.rating, x.cost_per_task))
        return matches
    
    def hire_agent(self, client_id: str, agent_listing: AgentListing, task: str):
        """Hire an agent through A2A protocol"""
        transaction = {
            "id": f"tx_{len(self.transactions)}",
            "client": client_id,
            "agent": agent_listing.agent_id,
            "vendor": agent_listing.vendor,
            "task": task,
            "cost": agent_listing.cost_per_task,
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        
        print(f"🤝 A2A Transaction: {client_id} hired {agent_listing.vendor}/{agent_listing.agent_id}")
        print(f"   Task: {task}")
        print(f"   Cost: ${agent_listing.cost_per_task:.2f}")
        
        return transaction

class KinicReputation:
    """Kinic tracks agent reputation and performance"""
    
    def __init__(self):
        self.performance_history = {}
        self.skill_success_rates = {}
    
    def record_performance(self, agent_id: str, skill: str, success: bool, time_taken: float):
        """Record agent performance for reputation tracking"""
        if agent_id not in self.performance_history:
            self.performance_history[agent_id] = []
            self.skill_success_rates[agent_id] = {}
        
        self.performance_history[agent_id].append({
            "skill": skill,
            "success": success,
            "time_taken": time_taken,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update skill-specific success rate
        if skill not in self.skill_success_rates[agent_id]:
            self.skill_success_rates[agent_id][skill] = {"success": 0, "total": 0}
        
        self.skill_success_rates[agent_id][skill]["total"] += 1
        if success:
            self.skill_success_rates[agent_id][skill]["success"] += 1
        
        success_rate = (self.skill_success_rates[agent_id][skill]["success"] / 
                       self.skill_success_rates[agent_id][skill]["total"] * 100)
        
        print(f"📊 Kinic: Updated {agent_id} reputation")
        print(f"   Skill: {skill} - Success rate: {success_rate:.1f}%")
    
    def get_agent_rating(self, agent_id: str):
        """Calculate agent's overall rating"""
        if agent_id not in self.performance_history:
            return 5.0  # Default rating for new agents
        
        total_success = sum(1 for p in self.performance_history[agent_id] if p["success"])
        total_tasks = len(self.performance_history[agent_id])
        
        if total_tasks == 0:
            return 5.0
        
        # Rating based on success rate (1-10 scale)
        return min(10, max(1, (total_success / total_tasks) * 10))
    
    def recommend_agent(self, skill_needed: str, available_agents: List[AgentListing]):
        """Recommend best agent based on historical performance"""
        recommendations = []
        
        for agent in available_agents:
            rating = self.get_agent_rating(agent.agent_id)
            
            # Check if agent has specific skill experience
            skill_performance = None
            if agent.agent_id in self.skill_success_rates:
                for skill in self.skill_success_rates[agent.agent_id]:
                    if skill_needed.lower() in skill.lower():
                        stats = self.skill_success_rates[agent.agent_id][skill]
                        skill_performance = stats["success"] / stats["total"] if stats["total"] > 0 else 0
                        break
            
            score = rating
            if skill_performance is not None:
                # Boost score if agent has proven skill experience
                score = rating * 0.7 + skill_performance * 10 * 0.3
            
            recommendations.append((agent, score))
        
        recommendations.sort(key=lambda x: -x[1])
        return recommendations[0][0] if recommendations else None

# Demo: Multi-Vendor Agent Marketplace
def demo_agent_marketplace():
    """
    Demonstrates a marketplace where agents from different vendors 
    can discover and hire each other based on skills and reputation.
    """
    print("=" * 70)
    print("DEMO: A2A + Kinic Multi-Vendor Agent Marketplace")
    print("=" * 70)
    
    # Initialize systems
    marketplace = A2AMarketplace()
    reputation = KinicReputation()
    
    # List agents from different vendors
    print("\n🏪 AGENT MARKETPLACE LISTINGS")
    print("-" * 50)
    
    agents = [
        # OpenAI Agents
        AgentListing(
            agent_id="gpt4-coder",
            vendor="OpenAI",
            model="gpt-4-turbo",
            skills=["Python development", "API design", "debugging", "code optimization"],
            cost_per_task=0.50
        ),
        AgentListing(
            agent_id="gpt35-assistant",
            vendor="OpenAI", 
            model="gpt-3.5-turbo",
            skills=["documentation", "testing", "simple scripts", "data processing"],
            cost_per_task=0.05
        ),
        
        # Anthropic Agents
        AgentListing(
            agent_id="claude-analyst",
            vendor="Anthropic",
            model="claude-3-opus",
            skills=["code review", "security analysis", "architecture design", "best practices"],
            cost_per_task=0.45
        ),
        AgentListing(
            agent_id="claude-researcher",
            vendor="Anthropic",
            model="claude-3-sonnet",
            skills=["research", "documentation", "technical writing", "API exploration"],
            cost_per_task=0.20
        ),
        
        # Perplexity Agents
        AgentListing(
            agent_id="pplx-searcher",
            vendor="Perplexity",
            model="llama-3.1-sonar-large",
            skills=["web search", "fact checking", "current events", "API documentation lookup"],
            cost_per_task=0.15
        ),
        
        # Cohere Agents
        AgentListing(
            agent_id="cohere-embedder",
            vendor="Cohere",
            model="embed-english-v3",
            skills=["semantic search", "document indexing", "similarity matching", "RAG"],
            cost_per_task=0.10
        )
    ]
    
    # List all agents on marketplace
    for agent in agents:
        marketplace.list_agent(agent)
        time.sleep(0.5)  # For demo effect
    
    # Simulate tasks that need to be done
    print("\n\n📝 INCOMING TASKS REQUIRING AGENTS")
    print("-" * 50)
    
    tasks = [
        {"client": "startup-team", "need": "Python API development", "budget": 0.60},
        {"client": "enterprise-corp", "need": "security analysis", "budget": 1.00},
        {"client": "student-project", "need": "simple documentation", "budget": 0.10},
        {"client": "research-lab", "need": "current AI trends search", "budget": 0.30},
        {"client": "dev-team", "need": "code review and optimization", "budget": 0.50},
    ]
    
    for task in tasks:
        print(f"\n🔍 Client: {task['client']}")
        print(f"   Needs: {task['need']}")
        print(f"   Budget: ${task['budget']:.2f}")
        
        # Discover agents that match the need
        candidates = marketplace.discover_by_skill(task['need'], max_cost=task['budget'])
        
        if candidates:
            # Kinic recommends based on reputation
            recommended = reputation.recommend_agent(task['need'], candidates)
            
            if recommended:
                print(f"   ✨ Kinic recommends: {recommended.vendor}/{recommended.agent_id}")
                
                # Hire the agent
                transaction = marketplace.hire_agent(
                    task['client'], 
                    recommended, 
                    task['need']
                )
                
                # Simulate task completion and record performance
                success = random.random() > 0.2  # 80% success rate
                time_taken = random.uniform(0.5, 3.0)
                
                reputation.record_performance(
                    recommended.agent_id,
                    task['need'],
                    success,
                    time_taken
                )
        else:
            print(f"   ❌ No agents available within budget")
    
    # Show marketplace statistics
    print("\n\n📈 MARKETPLACE STATISTICS")
    print("-" * 50)
    print(f"Total Agents Listed: {len(marketplace.listings)}")
    print(f"Total Transactions: {len(marketplace.transactions)}")
    
    # Show cross-vendor collaborations
    cross_vendor = []
    for tx in marketplace.transactions:
        client_vendor = tx['client'].split('-')[0]  # Simplified
        if tx['vendor'].lower() not in client_vendor.lower():
            cross_vendor.append(tx)
    
    print(f"Cross-Vendor Collaborations: {len(cross_vendor)}")
    
    if cross_vendor:
        print("\n🌐 Cross-Vendor Collaboration Examples:")
        for tx in cross_vendor[:3]:
            print(f"   • {tx['client']} → {tx['vendor']}/{tx['agent']} for {tx['task']}")
    
    # Show reputation leaders
    print("\n🏆 TOP RATED AGENTS")
    print("-" * 50)
    
    agent_ratings = [(a.agent_id, a.vendor, reputation.get_agent_rating(a.agent_id)) 
                     for a in agents]
    agent_ratings.sort(key=lambda x: -x[2])
    
    for agent_id, vendor, rating in agent_ratings[:3]:
        print(f"   ⭐ {vendor}/{agent_id}: {rating:.1f}/10")
    
    print("\n" + "=" * 70)
    print("✅ Marketplace Demo Complete")
    print("Key Achievement: Agents from different AI vendors successfully")
    print("discovered and collaborated through A2A protocol + Kinic reputation")
    print("=" * 70)

import time

if __name__ == "__main__":
    demo_agent_marketplace()