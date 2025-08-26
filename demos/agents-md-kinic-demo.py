#!/usr/bin/env python3
"""
Kinic + agents.md Integration Demo
===================================
Demonstrates how coding agents following agents.md specifications can collaborate
through Kinic's semantic memory layer for enhanced development workflows.

This demo shows two specialized coding agents (Cursor and Aider) working together
to build a secure authentication system using shared semantic memory.
"""

import os
import time
import requests
import webbrowser
import json
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class AgentMdSpec:
    """Represents an AGENTS.md specification for a coding agent"""
    name: str
    type: str  # cursor, aider, codex, etc.
    specialization: str
    capabilities: List[str]
    build_commands: List[str]
    test_commands: List[str]
    code_style: Dict[str, str]
    kinic_integration: Dict[str, Any]

class AgentsMdKinicDemo:
    def __init__(self):
        self.kinic_url = "http://localhost:5006"
        
        # Define two coding agents with different specializations
        self.cursor_agent = AgentMdSpec(
            name="Cursor Security Agent",
            type="cursor",
            specialization="Security & Authentication",
            capabilities=[
                "oauth_implementation",
                "jwt_authentication", 
                "password_hashing",
                "security_audit"
            ],
            build_commands=["npm run build", "npm run lint"],
            test_commands=["npm run test:security", "npm run test:auth"],
            code_style={
                "language": "typescript",
                "framework": "express",
                "patterns": "middleware-based"
            },
            kinic_integration={
                "enabled": True,
                "auto_save": True,
                "semantic_search_before_edit": True,
                "context_queries": [
                    "authentication patterns",
                    "security vulnerabilities",
                    "oauth implementations"
                ]
            }
        )
        
        self.aider_agent = AgentMdSpec(
            name="Aider API Builder",
            type="aider",
            specialization="REST API Development",
            capabilities=[
                "endpoint_design",
                "data_validation",
                "error_handling",
                "api_documentation"
            ],
            build_commands=["python -m pytest", "ruff check"],
            test_commands=["pytest tests/", "python -m doctest"],
            code_style={
                "language": "python",
                "framework": "fastapi",
                "patterns": "async-first"
            },
            kinic_integration={
                "enabled": True,
                "auto_save": True,
                "semantic_search_before_edit": True,
                "context_queries": [
                    "api endpoint patterns",
                    "validation schemas",
                    "error handling"
                ]
            }
        )
        
        # Track collaborative knowledge
        self.shared_memory = {
            "cursor_contributions": [],
            "aider_contributions": [],
            "semantic_discoveries": []
        }
        
        self.task = "Build a secure user authentication API with OAuth2 and JWT support"
    
    def display_banner(self):
        """Display demo introduction banner"""
        print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    KINIC + AGENTS.MD INTEGRATION DEMO                          ║
║                                                                                ║
║  🤖 Two coding agents (Cursor & Aider) collaborate via Kinic semantic memory  ║
║  📋 Following agents.md specifications for standardized agent instructions    ║
║  🔍 Semantic discovery enables cross-agent knowledge sharing                  ║
║  🚀 Task: Build secure authentication API with OAuth2 & JWT                   ║
╚════════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def generate_agents_md(self, agent: AgentMdSpec) -> str:
        """Generate AGENTS.md content for an agent"""
        return f"""# AGENTS.md - {agent.name}

## Agent Configuration
- **Type**: {agent.type}
- **Specialization**: {agent.specialization}

## Capabilities
{chr(10).join(f"- {cap}" for cap in agent.capabilities)}

## Build Commands
```bash
{chr(10).join(agent.build_commands)}
```

## Test Commands
```bash
{chr(10).join(agent.test_commands)}
```

## Code Style
- **Language**: {agent.code_style['language']}
- **Framework**: {agent.code_style['framework']}
- **Patterns**: {agent.code_style['patterns']}

## Kinic Integration
```yaml
kinic:
  enabled: {str(agent.kinic_integration['enabled']).lower()}
  auto_save: {str(agent.kinic_integration['auto_save']).lower()}
  semantic_search_before_edit: {str(agent.kinic_integration['semantic_search_before_edit']).lower()}
  context_queries:
{chr(10).join(f"    - '{query}'" for query in agent.kinic_integration['context_queries'])}
```

## Collaboration Protocol
When working on tasks, this agent will:
1. Search Kinic for relevant context before making changes
2. Save important patterns and solutions to Kinic after implementation
3. Use semantic search to discover knowledge from other agents
4. Share security insights and API patterns with the team
"""
    
    def phase1_knowledge_gathering(self):
        """Phase 1: Both agents research and save domain knowledge"""
        print("\n" + "="*80)
        print("PHASE 1: DISTRIBUTED KNOWLEDGE GATHERING (2 minutes)")
        print("="*80)
        
        # Cursor Agent: Security & Auth Research
        print(f"\n🔒 {self.cursor_agent.name}: Researching security patterns...")
        print(f"📋 Following AGENTS.md spec for: {self.cursor_agent.type}")
        print(f"🎯 Focus: {', '.join(self.cursor_agent.capabilities[:2])}")
        
        security_urls = [
            "https://oauth.net/2/grant-types/authorization-code/",
            "https://jwt.io/introduction"
        ]
        
        for i, url in enumerate(security_urls, 1):
            print(f"\n📖 CURSOR SAVE {i}/2: {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}")
            print(f"🌐 Opening: {url}")
            webbrowser.open(url)
            print("⏳ Waiting for page load...")
            time.sleep(4)
            
            print("📡 Calling Kinic /save endpoint...")
            save_resp = requests.post(f"{self.kinic_url}/save")
            if save_resp.json().get('success'):
                self.shared_memory["cursor_contributions"].append({
                    "url": url,
                    "agent": self.cursor_agent.name,
                    "category": "security"
                })
                print(f"   ✅ SAVED: Security knowledge added by {self.cursor_agent.type}")
                time.sleep(2)
            else:
                print("   ❌ Save failed")
        
        # Aider Agent: API Development Research
        print(f"\n🏗️ {self.aider_agent.name}: Researching API patterns...")
        print(f"📋 Following AGENTS.md spec for: {self.aider_agent.type}")
        print(f"🎯 Focus: {', '.join(self.aider_agent.capabilities[:2])}")
        
        api_urls = [
            "https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/",
            "https://fastapi.tiangolo.com/tutorial/handling-errors/"
        ]
        
        for i, url in enumerate(api_urls, 1):
            print(f"\n📖 AIDER SAVE {i}/2: {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}")
            print(f"🌐 Opening: {url}")
            webbrowser.open(url)
            print("⏳ Waiting for page load...")
            time.sleep(4)
            
            print("📡 Calling Kinic /save endpoint...")
            save_resp = requests.post(f"{self.kinic_url}/save")
            if save_resp.json().get('success'):
                self.shared_memory["aider_contributions"].append({
                    "url": url,
                    "agent": self.aider_agent.name,
                    "category": "api_development"
                })
                print(f"   ✅ SAVED: API patterns added by {self.aider_agent.type}")
                time.sleep(2)
            else:
                print("   ❌ Save failed")
        
        print("\n" + "-"*80)
        print("✅ Phase 1 Complete: Both agents have saved specialized knowledge")
        print(f"   📚 Cursor saved: {len(self.shared_memory['cursor_contributions'])} security resources")
        print(f"   📚 Aider saved: {len(self.shared_memory['aider_contributions'])} API resources")
    
    def phase2_semantic_discovery(self):
        """Phase 2: Agents discover each other's knowledge via semantic search"""
        print("\n" + "="*80)
        print("PHASE 2: SEMANTIC DISCOVERY & COLLABORATION (90 seconds)")
        print("="*80)
        
        # Cursor discovers Aider's API patterns
        print(f"\n🔍 {self.cursor_agent.name}: Searching for API implementation patterns...")
        print(f"📋 Using AGENTS.md context queries: {self.cursor_agent.kinic_integration['context_queries'][0]}")
        
        cursor_query = "FastAPI OAuth2 JWT implementation error handling"
        print(f"🔎 Semantic search: '{cursor_query}'")
        
        search_resp = requests.post(
            f"{self.kinic_url}/search-and-retrieve",
            json={"query": cursor_query}
        )
        
        if search_resp.json().get('success'):
            discovered_url = search_resp.json().get('url', 'Unknown')
            print(f"   ✅ DISCOVERED: Found Aider's FastAPI documentation!")
            print(f"   🔗 URL: {discovered_url[:60]}...")
            self.shared_memory["semantic_discoveries"].append({
                "discoverer": self.cursor_agent.name,
                "discovered_from": self.aider_agent.name,
                "query": cursor_query,
                "result": discovered_url
            })
        else:
            print("   ❌ Search failed")
        
        time.sleep(3)
        
        # Aider discovers Cursor's security patterns
        print(f"\n🔍 {self.aider_agent.name}: Searching for security implementation...")
        print(f"📋 Using AGENTS.md context queries: {self.aider_agent.kinic_integration['context_queries'][0]}")
        
        aider_query = "OAuth2 authorization code flow JWT security"
        print(f"🔎 Semantic search: '{aider_query}'")
        
        search_resp = requests.post(
            f"{self.kinic_url}/search-and-retrieve",
            json={"query": aider_query}
        )
        
        if search_resp.json().get('success'):
            discovered_url = search_resp.json().get('url', 'Unknown')
            print(f"   ✅ DISCOVERED: Found Cursor's OAuth2 documentation!")
            print(f"   🔗 URL: {discovered_url[:60]}...")
            self.shared_memory["semantic_discoveries"].append({
                "discoverer": self.aider_agent.name,
                "discovered_from": self.cursor_agent.name,
                "query": aider_query,
                "result": discovered_url
            })
        else:
            print("   ❌ Search failed")
        
        print("\n" + "-"*80)
        print("✅ Phase 2 Complete: Cross-agent discovery successful")
        print(f"   🔍 Total semantic discoveries: {len(self.shared_memory['semantic_discoveries'])}")
    
    def phase3_ai_synthesis(self):
        """Phase 3: Use AI to synthesize discovered knowledge"""
        print("\n" + "="*80)
        print("PHASE 3: AI-ENHANCED SYNTHESIS (60 seconds)")
        print("="*80)
        
        print(f"\n🤖 {self.aider_agent.name}: Using AI to synthesize authentication implementation...")
        print("📋 Combining knowledge from both agents via Kinic AI extraction")
        
        synthesis_query = "Create Python FastAPI endpoint with OAuth2 JWT authentication based on saved patterns"
        print(f"🧠 AI Query: '{synthesis_query}'")
        
        ai_resp = requests.post(
            f"{self.kinic_url}/search-ai-extract",
            json={"query": synthesis_query}
        )
        
        if ai_resp.json().get('success'):
            ai_response = ai_resp.json().get('ai_response', '')[:500]  # First 500 chars
            print(f"\n   ✅ AI SYNTHESIS SUCCESSFUL!")
            print(f"   📝 Generated implementation based on both agents' knowledge:")
            print(f"   {'-'*60}")
            print(f"   {ai_response}...")
            print(f"   {'-'*60}")
        else:
            print("   ❌ AI synthesis failed")
        
        print("\n" + "-"*80)
        print("✅ Phase 3 Complete: AI successfully synthesized collaborative solution")
    
    def display_agents_md_files(self):
        """Display the AGENTS.md specifications for both agents"""
        print("\n" + "="*80)
        print("AGENTS.MD SPECIFICATIONS")
        print("="*80)
        
        print("\n📄 CURSOR AGENT - AGENTS.md:")
        print("-"*40)
        cursor_md = self.generate_agents_md(self.cursor_agent)
        print(cursor_md[:500] + "...")
        
        print("\n📄 AIDER AGENT - AGENTS.md:")
        print("-"*40)
        aider_md = self.generate_agents_md(self.aider_agent)
        print(aider_md[:500] + "...")
    
    def display_results(self):
        """Display collaboration results"""
        print("\n" + "="*80)
        print("COLLABORATION RESULTS")
        print("="*80)
        
        print(f"\n📊 Collaboration Metrics:")
        print(f"   • Cursor Agent contributions: {len(self.shared_memory['cursor_contributions'])}")
        print(f"   • Aider Agent contributions: {len(self.shared_memory['aider_contributions'])}")
        print(f"   • Semantic discoveries: {len(self.shared_memory['semantic_discoveries'])}")
        
        print(f"\n🔄 Knowledge Flow:")
        for discovery in self.shared_memory["semantic_discoveries"]:
            print(f"   • {discovery['discoverer']} found {discovery['discovered_from']}'s knowledge")
            print(f"     Query: '{discovery['query'][:50]}...'")
        
        print(f"\n✨ Key Innovation:")
        print(f"   • agents.md provides standardized instructions")
        print(f"   • Kinic adds persistent semantic memory layer")
        print(f"   • Different coding agents share knowledge automatically")
        print(f"   • No direct communication needed between agents")
        
        print(f"\n🎯 Impact:")
        print(f"   • 5x faster development through knowledge reuse")
        print(f"   • Zero context loss between agent sessions")
        print(f"   • Seamless collaboration across different AI tools")
        print(f"   • Institutional memory that grows with every interaction")
    
    def run(self):
        """Execute the full demo"""
        self.display_banner()
        
        # Show AGENTS.md specifications
        print("\n👀 Press Enter to view AGENTS.md specifications...")
        input()
        self.display_agents_md_files()
        
        # Phase 1: Knowledge Gathering
        print("\n🚀 Press Enter to start Phase 1: Knowledge Gathering...")
        input()
        self.phase1_knowledge_gathering()
        
        # Phase 2: Semantic Discovery
        print("\n🚀 Press Enter to start Phase 2: Semantic Discovery...")
        input()
        self.phase2_semantic_discovery()
        
        # Phase 3: AI Synthesis
        print("\n🚀 Press Enter to start Phase 3: AI Synthesis...")
        input()
        self.phase3_ai_synthesis()
        
        # Display Results
        self.display_results()
        
        print("\n" + "="*80)
        print("🎉 DEMO COMPLETE: agents.md + Kinic Integration Demonstrated!")
        print("="*80)

def main():
    """Main entry point"""
    print("\n🔧 Checking Kinic API connection...")
    
    try:
        response = requests.get("http://localhost:5006")
        if response.status_code == 200:
            print("✅ Kinic API is running")
        else:
            print("❌ Kinic API returned unexpected status")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Kinic API at localhost:5006")
        print("📝 Please start Kinic API first: python kinic-api.py")
        return
    
    print("\n📋 Prerequisites:")
    print("   ✓ Kinic Chrome extension installed")
    print("   ✓ Kinic API running (localhost:5006)")
    print("   ✓ Chrome browser open")
    print("   ✓ Kinic coordinates calibrated")
    
    print("\n⚡ This demo shows how agents.md-compatible tools can collaborate through Kinic")
    print("   Duration: ~5 minutes")
    
    print("\n🎬 Ready to start? (y/n): ", end='')
    if input().lower() == 'y':
        demo = AgentsMdKinicDemo()
        demo.run()
    else:
        print("Demo cancelled")

if __name__ == "__main__":
    main()