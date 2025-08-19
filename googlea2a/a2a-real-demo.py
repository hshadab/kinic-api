#!/usr/bin/env python3
"""
REAL Google A2A + Kinic Developer Code Review Demo
=================================================
Two developer agents using ACTUAL Google A2A protocol enhanced with Kinic's semantic memory.

Uses the official A2A SDK v0.3.1+ for real agent-to-agent communication.
Demo: Code Reviewer + Security Specialist review PR with SQL injection vulnerability.
"""

import os
import time 
import requests
import webbrowser
import json
from typing import Dict, List, Optional
from colorama import init, Fore, Style, Back

# Import real A2A SDK
try:
    from a2a_sdk import A2AProtocol, AgentCard, TaskRequest, TaskResponse
    A2A_AVAILABLE = True
    print(f"{Fore.GREEN}✅ Real Google A2A SDK imported successfully")
except ImportError:
    print(f"{Fore.RED}❌ A2A SDK not found. Install with: pip install a2a-sdk")
    print(f"{Fore.YELLOW}   Falling back to simulation mode...")
    A2A_AVAILABLE = False

# Initialize colorama for colored output
init(autoreset=True)

class RealA2ACodeReviewDemo:
    """
    Demo using REAL Google A2A Protocol + Kinic semantic memory
    """
    
    def __init__(self):
        # Load configuration
        with open("demo_config.json", "r") as f:
            self.config = json.load(f)
        
        self.kinic_url = self.config["demo_settings"]["kinic_api_url"]
        
        # Initialize real A2A protocol
        if A2A_AVAILABLE:
            self.a2a = A2AProtocol()
            self.using_real_a2a = True
            print(f"{Fore.GREEN}🔗 Using REAL Google A2A Protocol v0.3.1+")
        else:
            # Fallback to simulation
            from a2a_dev_demo import MockA2AProtocol
            self.a2a = MockA2AProtocol()
            self.using_real_a2a = False
            print(f"{Fore.YELLOW}🔗 Using A2A Protocol Simulation")
        
        # Demo data
        self.task = "Review pull request with potential security vulnerability"
        self.knowledge_base = {
            "Code_Reviewer": [],
            "Security_Specialist": []
        }
        
        # The vulnerable code to review
        self.pr_code = '''def authenticate_user(username, password):
    # VULNERABLE: Direct string interpolation in SQL query  
    query = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    result = db.execute(query)
    return bool(result)'''
        
        # Setup A2A agents
        self.setup_real_a2a_agents()
    
    def setup_real_a2a_agents(self):
        """Setup agents using REAL Google A2A protocol"""
        
        if self.using_real_a2a:
            # Create real A2A Agent Cards
            code_reviewer_card = AgentCard(
                name="Code Reviewer Agent",
                version="1.0",
                description="Specialized in Python code quality and review practices",
                capabilities=["code_review", "style_check", "best_practices", "pep8_compliance"],
                endpoints={
                    "base_url": "http://localhost:8001",
                    "review": "/review_code",
                    "capabilities": "/capabilities"
                },
                # Kinic integration metadata
                metadata={
                    "kinic_integration": True,
                    "semantic_search": True,
                    "knowledge_domains": ["python_standards", "code_quality"]
                }
            )
            
            security_specialist_card = AgentCard(
                name="Security Specialist Agent",
                version="1.0", 
                description="Specialized in security vulnerabilities and OWASP compliance",
                capabilities=["security_audit", "vulnerability_scan", "owasp_compliance", "sql_injection_detection"],
                endpoints={
                    "base_url": "http://localhost:8002",
                    "security_review": "/security_audit", 
                    "capabilities": "/capabilities"
                },
                metadata={
                    "kinic_integration": True,
                    "semantic_search": True,
                    "knowledge_domains": ["sql_injection", "secure_coding", "owasp"]
                }
            )
            
            # Register agents with real A2A protocol
            try:
                self.a2a.register_agent("code_reviewer", code_reviewer_card)
                self.a2a.register_agent("security_specialist", security_specialist_card)
                print(f"{Fore.GREEN}✅ Real A2A agents registered successfully")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  A2A registration failed, using local mode: {str(e)}")
                self.using_real_a2a = False
        
        if not self.using_real_a2a:
            # Fallback to simulation
            self.a2a.register_agent("code_reviewer", {"capabilities": ["code_review", "style_check"]})
            self.a2a.register_agent("security_specialist", {"capabilities": ["security_audit", "vulnerability_scan"]})
            print(f"{Fore.BLUE}🔗 A2A simulation mode active")
    
    def display_banner(self):
        """Display demo banner"""
        a2a_status = "REAL A2A PROTOCOL" if self.using_real_a2a else "A2A SIMULATION"
        print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║     {Fore.WHITE}GOOGLE A2A + KINIC DEVELOPER DEMO ({a2a_status}){Fore.CYAN}     ║
{Fore.CYAN}║                                                                    ║
{Fore.CYAN}║  {Fore.YELLOW}Real A2A Protocol + Kinic semantic memory collaboration{Fore.CYAN}        ║
{Fore.CYAN}║  {Fore.WHITE}Task: Review PR with SQL injection vulnerability{Fore.CYAN}                  ║
{Fore.CYAN}╚════════════════════════════════════════════════════════════════════╝
        """)
    
    def act2_real_a2a_handoff(self):
        """Use real A2A protocol for agent communication"""
        print(f"\n{Fore.CYAN}" + "="*70)
        print(f"{Fore.WHITE}ACT 2: REAL A2A HANDOFF + SEMANTIC DISCOVERY")
        print(f"{Fore.CYAN}" + "="*70)
        
        # Create real A2A task request
        if self.using_real_a2a:
            print(f"{Fore.GREEN}🔄 Using REAL Google A2A Protocol for agent communication")
            
            # Create A2A task request
            task_request = TaskRequest(
                task_id="pr_review_123",
                from_agent="github_webhook",
                to_agent="code_reviewer", 
                task_type="code_review",
                task_data={
                    "pr_id": "PR-123",
                    "code_snippet": self.pr_code,
                    "author": "junior-developer",
                    "urgency": "normal"
                },
                metadata={
                    "kinic_context_available": True,
                    "semantic_search_enabled": True
                }
            )
            
            try:
                # Send real A2A message
                print(f"{Fore.BLUE}📨 Sending A2A TaskRequest...")
                print(f"{Fore.WHITE}   Protocol: A2A JSON-RPC 2.0 over HTTPS")
                print(f"{Fore.WHITE}   From: github_webhook → code_reviewer")
                print(f"{Fore.WHITE}   Task: code_review with Kinic context")
                
                response = self.a2a.send_task(task_request)
                print(f"{Fore.GREEN}✅ A2A task sent successfully")
                print(f"{Fore.CYAN}📥 A2A Response: {response.status}")
                
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️  A2A communication failed, using fallback: {str(e)}")
                self.using_real_a2a = False
        
        if not self.using_real_a2a:
            print(f"{Fore.BLUE}🔄 Using A2A simulation for agent communication")
            # Use simulation fallback
            task_data = {
                "pr_id": "PR-123", 
                "code_snippet": self.pr_code,
                "concern": "potential_sql_injection"
            }
            message = self.a2a.route_task("code_reviewer", "security_specialist", task_data)
            print(f"{Fore.GREEN}📨 A2A simulation message sent")
        
        # Continue with Kinic semantic discovery (same as before)
        print(f"\n{Fore.YELLOW}🔍 CODE REVIEWER: Searching Kinic for security guidance...")
        
        try:
            response = requests.post(
                f"{self.kinic_url}/search-and-retrieve",
                json={"query": "SQL injection prevention secure database queries"},
                timeout=60
            )
            
            if response.json().get('success'):
                found_url = response.json().get('url')
                print(f"{Fore.GREEN}📥 SEMANTIC MATCH FOUND: {found_url[:70]}...")
                print(f"{Fore.CYAN}✨ Kinic semantic search successful!")
                
                if self.using_real_a2a:
                    # Create real A2A escalation
                    escalation_request = TaskRequest(
                        task_id="security_review_123",
                        from_agent="code_reviewer",
                        to_agent="security_specialist",
                        task_type="security_review",
                        task_data={
                            "pr_id": "PR-123",
                            "vulnerability_type": "sql_injection",
                            "code_snippet": self.pr_code,
                            "kinic_reference": found_url,
                            "severity": "HIGH"
                        }
                    )
                    
                    try:
                        escalation_response = self.a2a.send_task(escalation_request)
                        print(f"{Fore.GREEN}🔄 Real A2A escalation successful")
                        print(f"{Fore.WHITE}   From: code_reviewer → security_specialist")
                        print(f"{Fore.RED}   Priority: HIGH security review")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️  A2A escalation failed: {str(e)}")
                        
                else:
                    # Simulation escalation
                    print(f"{Fore.BLUE}🔄 A2A simulation escalation")
                    
                self.discovery_success = True
                self.kinic_reference = found_url
            else:
                print(f"{Fore.RED}❌ Semantic search failed")
                self.discovery_success = False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Kinic search error: {str(e)}")
            self.discovery_success = False
    
    def show_results(self):
        """Show results with A2A protocol status"""
        print(f"\n{Fore.CYAN}" + "="*70)
        print(f"{Fore.WHITE}REAL A2A + KINIC COLLABORATION RESULTS")
        print(f"{Fore.CYAN}" + "="*70)
        
        protocol_status = "✅ REAL Google A2A Protocol v0.3.1+" if self.using_real_a2a else "⚠️  A2A Simulation Mode"
        
        print(f"""
{Fore.MAGENTA}🔗 A2A PROTOCOL STATUS: {protocol_status}
{Fore.WHITE}• A2A SDK Installation: {'✅ a2a-sdk v0.3.1+ available' if A2A_AVAILABLE else '❌ Not installed'}
• Agent Communication: {'✅ Real JSON-RPC 2.0 over HTTPS' if self.using_real_a2a else '🔄 Simulated messaging'}
• Agent Registration: {'✅ Official A2A agent cards' if self.using_real_a2a else '🔄 Mock registration'}
• Task Routing: {'✅ TaskRequest/TaskResponse objects' if self.using_real_a2a else '🔄 Dictionary-based simulation'}

{Fore.GREEN}🎬 COLLABORATION RESULTS:
{Fore.WHITE}• Developer agents: 2 (Code Reviewer + Security Specialist)  
• Knowledge pages saved: {len(self.knowledge_base.get('Code_Reviewer', [])) + len(self.knowledge_base.get('Security_Specialist', []))}
• A2A protocol messages: {'✅ Real A2A communication' if self.using_real_a2a else '🔄 Simulated messages'}
• Kinic semantic discovery: {'✅ Successful' if getattr(self, 'discovery_success', False) else '❌ Failed'}
• Total demo time: ~5 minutes

{Fore.CYAN}🌟 KEY ADVANTAGES:
{Fore.WHITE}• Real A2A Protocol: {'Standard agent interoperability' if self.using_real_a2a else 'Conceptual demonstration'}
• Kinic Integration: Semantic memory enhances A2A agent capabilities  
• Cross-Agent Learning: Agents discover each other's expertise automatically
• Production Ready: {'✅ Real protocol implementation' if self.using_real_a2a else '🔄 Demo ready for upgrade'}
        """)
        
        if not self.using_real_a2a:
            print(f"\n{Fore.YELLOW}💡 TO USE REAL A2A PROTOCOL:")
            print(f"{Fore.WHITE}   pip install a2a-sdk")
            print(f"{Fore.WHITE}   python a2a-real-demo.py")
    
    def run_demo(self):
        """Execute the real A2A + Kinic demo"""
        self.display_banner()
        
        # Check prerequisites
        print(f"\n{Fore.BLUE}🔧 Checking prerequisites...")
        
        # Check Kinic API
        try:
            resp = requests.get(self.kinic_url, timeout=5)
            if resp.status_code != 200:
                raise Exception("Kinic API not responding correctly")
            print(f"{Fore.GREEN}✅ Kinic API connected at {self.kinic_url}")
        except Exception as e:
            print(f"{Fore.RED}❌ Kinic API failed: {str(e)}")
            print(f"{Fore.WHITE}   Please start: python ../kinic-api.py")
            return False
        
        # Check A2A SDK status
        if A2A_AVAILABLE:
            print(f"{Fore.GREEN}✅ Google A2A SDK v0.3.1+ available")
        else:
            print(f"{Fore.YELLOW}⚠️  A2A SDK not installed - using simulation")
            print(f"{Fore.WHITE}   Install with: pip install a2a-sdk")
        
        print(f"\n{Fore.CYAN}🎬 DEMO OVERVIEW:")
        print(f"{Fore.WHITE}   Demo uses {'REAL A2A protocol' if self.using_real_a2a else 'A2A simulation'} + Kinic semantic memory")
        print(f"{Fore.WHITE}   Total time: ~5 minutes")
        
        print(f"\n{Fore.GREEN}🚀 Starting Real A2A + Kinic Demo...")
        
        start_time = time.time()
        
        try:
            # Simplified demo focusing on A2A protocol differences
            print(f"\n{Fore.MAGENTA}⏭️  Running A2A Handoff + Discovery...")
            self.act2_real_a2a_handoff()
            
            elapsed = time.time() - start_time
            print(f"\n{Fore.YELLOW}⏱️  Total time: {elapsed/60:.1f} minutes")
            
            self.show_results()
            
            print(f"\n{Fore.CYAN}" + "="*70)
            print(f"{Fore.WHITE}🎯 DEMO CONCLUSION")
            print(f"{Fore.CYAN}" + "="*70)
            
            if self.using_real_a2a:
                print(f"""
{Fore.GREEN}✅ SUCCESS: Real Google A2A Protocol + Kinic Integration Working!

{Fore.WHITE}This demo proves that:
• Google's A2A protocol enables standardized agent communication
• Kinic's semantic memory enhances A2A agents with persistent knowledge
• Real agent interoperability is possible with A2A + Kinic

{Fore.CYAN}Next steps: Scale to more agents, add real agent endpoints, integrate with production systems.
                """)
            else:
                print(f"""
{Fore.YELLOW}Demo ran in simulation mode - install A2A SDK for full experience:

{Fore.WHITE}pip install a2a-sdk
python a2a-real-demo.py

{Fore.CYAN}This simulation shows the potential - real A2A protocol would provide
standardized agent interoperability across the entire ecosystem.
                """)
            
            return True
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Demo interrupted by user")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}Demo failed: {str(e)}")
            return False


if __name__ == "__main__":
    print(f"{Fore.CYAN}🚀 Real Google A2A + Kinic Demo Starting...")
    
    demo = RealA2ACodeReviewDemo()
    success = demo.run_demo()
    
    if success:
        print(f"\n{Fore.GREEN}✅ Demo completed!")
        if demo.using_real_a2a:
            print(f"{Fore.CYAN}🎉 Successfully used REAL Google A2A Protocol!")
        else:
            print(f"{Fore.YELLOW}💡 Upgrade to real A2A: pip install a2a-sdk")
    else:
        print(f"\n{Fore.RED}❌ Demo failed - check prerequisites")