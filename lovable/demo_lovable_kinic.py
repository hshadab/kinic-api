#!/usr/bin/env python3
"""
Lovable.dev + Kinic Memory Integration Demo

This demo shows how Kinic's persistent AI memory solves Lovable's 
session memory problem, enabling true continuity across development sessions.

Demo Flow:
1. Simulate Day 1: Building an app with Lovable
2. Show memory being stored in Kinic
3. Simulate Day 2: Continuing development with full context
4. Demonstrate pattern learning and smart suggestions
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from kinic_api import KinicMemoryAPI


class LovableKinicDemo:
    """
    Demonstration of Lovable.dev enhanced with Kinic memory
    """
    
    def __init__(self):
        # Simulate an org with two users working across two projects
        self.org_id = "acme-corp"
        self.dev_a = KinicMemoryAPI(agent_id="lovable-assistant", org_id=self.org_id, user_id="dev_a")
        self.dev_b = KinicMemoryAPI(agent_id="lovable-assistant", org_id=self.org_id, user_id="dev_b")
        self.project_a = "ecommerce-mvp"
        self.repo_a = "github.com/acme/ecommerce-mvp"
        self.project_b = "blog-platform"
        self.repo_b = "github.com/acme/blog-platform"
        # Defaults for the narrative
        self.current_project = self.project_a
        
    def simulate_day_1_development(self):
        """Simulate first day of development with Lovable"""
        print("\n" + "="*60)
        print("🚀 DAY 1: Starting new e-commerce project in Lovable")
        print("="*60 + "\n")
        
        # User starts building
        print("👤 User: 'Build me an e-commerce app with user authentication'\n")
        time.sleep(1)
        
        # Lovable builds the app
        print("🤖 Lovable: Creating e-commerce app structure...")
        print("   ✓ Setting up React with TypeScript")
        print("   ✓ Installing Tailwind CSS")
        print("   ✓ Adding Supabase for authentication")
        print("   ✓ Creating product catalog structure\n")
        time.sleep(1)
        
        # Store decisions in Kinic
        print("🧠 Kinic: Storing architectural decisions...")
        
        decisions = [
            {
                "type": "architecture",
                "content": "Chose React with TypeScript for type safety",
                "context": "User building e-commerce MVP",
                "metadata": {"project": self.current_project, "day": 1}
            },
            {
                "type": "styling",
                "content": "Using Tailwind CSS for utility-first styling",
                "context": "Rapid prototyping requirement",
                "metadata": {"project": self.current_project, "day": 1}
            },
            {
                "type": "authentication",
                "content": "Implemented Supabase Auth with email/password",
                "context": "User requested authentication",
                "metadata": {"project": self.current_project, "day": 1}
            },
            {
                "type": "database",
                "content": "Supabase PostgreSQL for data persistence",
                "context": "Already using Supabase for auth",
                "metadata": {"project": self.current_project, "day": 1}
            },
            {
                "type": "pattern",
                "content": "User prefers async/await over .then() chains",
                "confidence": 0.8,
                "examples": ["fetchProducts", "authenticateUser", "loadCart"],
                "metadata": {"project": self.current_project, "day": 1}
            }
        ]
        
        # Dev A working on Project A
        self.dev_a.set_context(project=self.project_a, repo=self.repo_a)
        for decision in decisions:
            result = self.dev_a.store_memory(decision)
            print(f"   ✓ Stored: {decision['content'][:50]}...")
            time.sleep(0.5)

        # Add org-wide standards and snippets
        print("\n🧭 Kinic: Recording org standards and reusable snippets...")
        self.dev_a.store_standard("ui.framework", "tailwind-css", scope="org")
        self.dev_a.store_standard("react.state", "prefer-context-over-redux", scope="org")
        self.dev_a.store_snippet(
            title="Supabase auth helper",
            language="ts",
            code=(
                "export async function requireAuth(client){\n"
                "  const { data } = await client.auth.getUser();\n"
                "  if(!data.user) throw new Error('not-authenticated');\n"
                "  return data.user;\n"
                "}"
            ),
            project=self.project_a,
            repo=self.repo_a,
        )
        
        print("\n✅ Day 1 Complete: Basic e-commerce app created")
        print("📊 Memories stored: 5 decisions and patterns")
        
        return len(decisions)
    
    def simulate_session_break(self):
        """Simulate closing Lovable and time passing"""
        print("\n" + "="*60)
        print("💤 SESSION ENDED - Browser closed")
        print("⏰ 24 hours pass...")
        print("="*60 + "\n")
        time.sleep(2)
    
    def simulate_day_2_without_kinic(self):
        """Show what happens without Kinic (current Lovable limitation)"""
        print("\n" + "="*60)
        print("😞 DAY 2 WITHOUT KINIC: The Current Problem")
        print("="*60 + "\n")
        
        print("👤 User: 'Add a shopping cart with checkout flow'\n")
        time.sleep(1)
        
        print("🤖 Lovable: 'I don't have access to yesterday's conversation.")
        print("           Should I use Firebase, Supabase, or Auth0 for authentication?")
        print("           What styling framework would you prefer?")
        print("           What database are you using?'\n")
        time.sleep(1)
        
        print("👤 User: 'We already chose Supabase and Tailwind yesterday!'\n")
        time.sleep(1)
        
        print("🤖 Lovable: 'I don't see that context. Let me start fresh...'\n")
        
        print("❌ Result: User must re-explain everything")
        print("⏱️  Time wasted: ~10-15 minutes per session")
    
    def simulate_day_2_with_kinic(self):
        """Show the enhanced experience with Kinic memory"""
        print("\n" + "="*60)
        print("✨ DAY 2 WITH KINIC: The Solution")
        print("="*60 + "\n")
        
        print("👤 User: 'Add a shopping cart with checkout flow'\n")
        time.sleep(1)
        
        # Kinic retrieves context
        print("🧠 Kinic: Retrieving relevant context...")
        context = self.dev_a.retrieve_memory({
            "project": self.project_a,
            "recent": 10
        })
        time.sleep(1)
        
        print("🤖 Lovable + Kinic: 'I remember your project! Continuing with:'")
        print("   • React + TypeScript structure")
        print("   • Tailwind CSS for styling")
        print("   • Supabase for auth and database")
        print("   • Your preference for async/await patterns\n")
        time.sleep(1)
        
        print("   Creating shopping cart with:")
        print("   ✓ Cart state management using React Context")
        print("   ✓ Supabase table for cart persistence")
        print("   ✓ Tailwind components matching yesterday's style")
        print("   ✓ Async/await for all API calls (your preference)")
        print("   ✓ Checkout flow integrated with existing Supabase auth\n")
        
        # Store new decisions
        new_decisions = [
            {
                "type": "feature",
                "content": "Shopping cart using React Context API",
                "context": "Maintaining state management consistency",
                "metadata": {"project": self.current_project, "day": 2}
            },
            {
                "type": "pattern",
                "content": "User consistently chooses React built-in solutions over external libraries",
                "confidence": 0.9,
                "metadata": {"project": self.current_project, "day": 2}
            }
        ]
        
        for decision in new_decisions:
            self.dev_a.store_memory(decision)
        
        print("✅ Result: Seamless continuation")
        print("⏱️  Time saved: 10-15 minutes")
        print("🎯 Consistency: 100% maintained")
    
    def demonstrate_pattern_learning(self):
        """Show how Kinic learns patterns over time"""
        print("\n" + "="*60)
        print("🎓 PATTERN LEARNING: Kinic Gets Smarter")
        print("="*60 + "\n")
        
        # Analyze patterns
        patterns = [m for m in self.dev_a.memory_store if m.get("type") == "pattern"]
        
        print("🧠 Kinic has learned your patterns:")
        for pattern in patterns:
            confidence = pattern.get("confidence", 0.5)
            print(f"   • {pattern['content']}")
            print(f"     Confidence: {'█' * int(confidence * 10)}{'░' * (10 - int(confidence * 10))} {confidence:.0%}\n")
        
        time.sleep(1)
        
        print("🤖 Lovable + Kinic: 'Based on your patterns, I'll automatically:'")
        print("   • Use async/await for all new API calls")
        print("   • Prefer React built-in solutions")
        print("   • Maintain Tailwind utility classes")
        print("   • Keep consistent error handling patterns")
    
    def show_memory_stats(self):
        """Display memory statistics"""
        print("\n" + "="*60)
        print("📊 MEMORY STATISTICS")
        print("="*60 + "\n")
        
        context = self.dev_a.get_context_for_session()
        
        print(f"Total Memories Stored: {context['total_memories']}")
        print(f"Session ID: {context['session_id']}")
        print(f"Agent ID: {context['agent_id']}")
        
        # Count by type
        memory_types = {}
        for memory in self.dev_a.memory_store:
            mem_type = memory.get("type", "unknown")
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1
        
        print("\nMemory Types:")
        for mem_type, count in memory_types.items():
            print(f"   • {mem_type}: {count}")
    
    def demonstrate_cross_project_memory(self):
        """Show how memory works across projects"""
        print("\n" + "="*60)
        print("🔄 CROSS-PROJECT INTELLIGENCE")
        print("="*60 + "\n")
        
        print("👤 User: 'Start a new blog project'\n")
        time.sleep(1)
        # Dev B starts Project B and benefits from org memory created by Dev A
        self.dev_b.set_context(project=self.project_b, repo=self.repo_b)

        print("🧠 Kinic: Applying learned preferences from previous projects...")
        org_memories = [m for m in (self.dev_a.memory_store + self.dev_b.memory_store) if m.get("type") in {"standard", "pattern", "snippet"}]
        # Dev B stores decisions influenced by org memory
        self.dev_b.store_decision("Use React + TypeScript", project=self.project_b, repo=self.repo_b)
        self.dev_b.store_decision("Use Tailwind CSS", project=self.project_b, repo=self.repo_b)
        self.dev_b.store_decision("Use Supabase for auth and DB", project=self.project_b, repo=self.repo_b)
        self.dev_b.store_pattern("Prefers async/await for async logic", confidence=0.85, project=self.project_b, repo=self.repo_b)

        print("\n🤖 Lovable + Kinic: 'Starting blog with your preferences:'")
        print("   • React + TypeScript (carried from org memory)")
        print("   • Tailwind CSS (org standard)")
        print("   • Supabase (consistent with past success)")
        print("   • Async/await patterns (learned preference)")
        print("\nNo need to re-specify - I remember how your team likes to build!")

        # Simulate bug in Project A and its fix, later reused in Project B
        print("\n🐛 Capturing incident and propagating fix across projects...")
        bug = self.dev_a.store_bug("Race condition in cart update when concurrent requests", severity="high", project=self.project_a, repo=self.repo_a)
        fix = self.dev_a.store_fix("Add server-side transaction + optimistic UI rollback", relates_to=bug["memory_id"], project=self.project_a, repo=self.repo_a)
        self.dev_b.store_pr_note("Apply cart transaction pattern from ecommerce-mvp to blog drafts", outcome="suggestion", project=self.project_b, repo=self.repo_b)
    
    def export_demo_data(self):
        """Export memory data for visualization"""
        # Merge memory across users for export (org-wide memory)
        export_data = {
            "org_id": self.org_id,
            "export_date": datetime.now().isoformat(),
            "projects": [self.project_a, self.project_b],
            "repos": [self.repo_a, self.repo_b],
            "memories": self.dev_a.memory_store + self.dev_b.memory_store,
            "total_count": len(self.dev_a.memory_store) + len(self.dev_b.memory_store),
        }
        
        # Save to file for visualization
        with open('demo_memory_export.json', 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n📁 Memory data exported to demo_memory_export.json")
        return export_data
    
    def run_full_demo(self):
        """Run the complete demonstration"""
        print("\n" + "🚀"*30)
        print("\n   LOVABLE.DEV + KINIC MEMORY INTEGRATION DEMO")
        print("\n" + "🚀"*30)
        
        # Day 1
        memories_created = self.simulate_day_1_development()
        
        # Break between sessions
        self.simulate_session_break()
        
        # Show the problem
        self.simulate_day_2_without_kinic()
        
        time.sleep(2)
        
        # Show the solution
        self.simulate_day_2_with_kinic()
        
        time.sleep(2)
        
        # Show pattern learning
        self.demonstrate_pattern_learning()
        
        time.sleep(2)
        
        # Show cross-project benefits
        self.demonstrate_cross_project_memory()
        
        time.sleep(2)
        
        # Show statistics
        self.show_memory_stats()
        
        # Export data
        export_data = self.export_demo_data()
        
        print("\n" + "="*60)
        print("🎯 DEMO COMPLETE")
        print("="*60)
        print("\n✨ Key Benefits Demonstrated:")
        print("   1. ✅ Perfect session-to-session continuity")
        print("   2. ✅ Automatic pattern learning")
        print("   3. ✅ Cross-project intelligence")
        print("   4. ✅ Zero manual context management")
        print("   5. ✅ 10-15 minutes saved per session")
        
        return export_data


def main():
    """Run the demo"""
    demo = LovableKinicDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
