#!/usr/bin/env python3
"""
A2A + Kinic Demo: Real-Time Incident Response System
=====================================================
Shows how A2A protocol coordinates urgent response while Kinic provides 
historical context and learns from each incident.

UNIQUE CAPABILITIES:
1. Dynamic team assembly based on incident type
2. Historical pattern recognition for faster resolution
3. Knowledge accumulation - each incident makes response better
4. Cross-team learning and best practice sharing
"""

import time
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum

class IncidentSeverity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Incident:
    """Represents a system incident"""
    def __init__(self, incident_id: str, type: str, severity: IncidentSeverity, 
                 symptoms: List[str], affected_systems: List[str]):
        self.id = incident_id
        self.type = type
        self.severity = severity
        self.symptoms = symptoms
        self.affected_systems = affected_systems
        self.status = "NEW"
        self.responders = []
        self.resolution_steps = []
        self.root_cause = None
        self.time_to_resolve = None
        self.created_at = datetime.now()

class A2AIncidentCoordinator:
    """A2A Protocol coordinator for incident response"""
    
    def __init__(self):
        self.active_incidents = {}
        self.available_responders = {}
        self.escalation_chains = {
            IncidentSeverity.CRITICAL: ["ops-lead", "security-chief", "cto"],
            IncidentSeverity.HIGH: ["senior-sre", "security-analyst"],
            IncidentSeverity.MEDIUM: ["sre", "developer"],
            IncidentSeverity.LOW: ["junior-sre"]
        }
    
    def register_responder(self, responder_id: str, skills: List[str], 
                          availability: str = "available"):
        """Register an incident responder"""
        self.available_responders[responder_id] = {
            "skills": skills,
            "availability": availability,
            "current_incident": None
        }
        print(f"👤 A2A: Registered responder {responder_id}")
        print(f"   Skills: {', '.join(skills)}")
    
    def trigger_incident(self, incident: Incident):
        """Trigger incident response via A2A protocol"""
        self.active_incidents[incident.id] = incident
        
        print(f"\n🚨 A2A: INCIDENT TRIGGERED - {incident.id}")
        print(f"   Type: {incident.type}")
        print(f"   Severity: {incident.severity.name}")
        print(f"   Symptoms: {', '.join(incident.symptoms[:2])}...")
        
        # Assemble response team based on severity
        response_team = self.assemble_team(incident)
        incident.responders = response_team
        
        print(f"   📞 Paging response team: {', '.join(response_team)}")
        
        return response_team
    
    def assemble_team(self, incident: Incident) -> List[str]:
        """Dynamically assemble response team"""
        team = []
        required_roles = self.escalation_chains.get(incident.severity, [])
        
        for role in required_roles:
            # Find available responder with matching skills
            for responder_id, info in self.available_responders.items():
                if info["availability"] == "available" and not info["current_incident"]:
                    # Check if responder has relevant skills
                    if any(skill in incident.type.lower() for skill in info["skills"]):
                        team.append(responder_id)
                        info["current_incident"] = incident.id
                        info["availability"] = "responding"
                        break
        
        return team
    
    def handoff(self, incident_id: str, from_responder: str, to_responder: str, reason: str):
        """Hand off incident between responders"""
        print(f"🔄 A2A Handoff: {from_responder} → {to_responder}")
        print(f"   Reason: {reason}")
        
        if incident_id in self.active_incidents:
            incident = self.active_incidents[incident_id]
            if from_responder in incident.responders:
                incident.responders.remove(from_responder)
            incident.responders.append(to_responder)

class KinicIncidentMemory:
    """Kinic stores and learns from incident history"""
    
    def __init__(self):
        self.incident_history = []
        self.resolution_patterns = {}
        self.mttr_by_type = {}  # Mean Time To Resolve
        self.successful_strategies = {}
    
    def search_similar_incidents(self, incident: Incident) -> List[Dict]:
        """Find similar past incidents"""
        similar = []
        
        for past_incident in self.incident_history:
            # Calculate similarity score
            score = 0
            
            # Type match
            if incident.type in past_incident["type"]:
                score += 3
            
            # Symptom overlap
            symptom_overlap = len(set(incident.symptoms) & set(past_incident.get("symptoms", [])))
            score += symptom_overlap
            
            # System overlap
            system_overlap = len(set(incident.affected_systems) & 
                               set(past_incident.get("affected_systems", [])))
            score += system_overlap
            
            if score > 2:  # Threshold for similarity
                similar.append({
                    "incident": past_incident,
                    "similarity_score": score
                })
        
        similar.sort(key=lambda x: -x["similarity_score"])
        
        if similar:
            print(f"📚 Kinic: Found {len(similar)} similar past incidents")
            print(f"   Most similar: {similar[0]['incident']['id']} (score: {similar[0]['similarity_score']})")
        
        return similar[:5]
    
    def get_recommended_solution(self, incident: Incident) -> Optional[Dict]:
        """Get recommended solution based on past incidents"""
        similar = self.search_similar_incidents(incident)
        
        if similar:
            # Get the most successful resolution
            best_resolution = similar[0]["incident"]
            
            if best_resolution.get("resolution_steps"):
                print(f"💡 Kinic: Recommending solution from {best_resolution['id']}")
                print(f"   Resolution time: {best_resolution.get('time_to_resolve', 'unknown')}")
                return {
                    "steps": best_resolution["resolution_steps"],
                    "root_cause": best_resolution.get("root_cause"),
                    "estimated_time": best_resolution.get("time_to_resolve")
                }
        
        return None
    
    def record_resolution(self, incident: Incident):
        """Record incident resolution for future learning"""
        incident_record = {
            "id": incident.id,
            "type": incident.type,
            "severity": incident.severity.name,
            "symptoms": incident.symptoms,
            "affected_systems": incident.affected_systems,
            "responders": incident.responders,
            "resolution_steps": incident.resolution_steps,
            "root_cause": incident.root_cause,
            "time_to_resolve": incident.time_to_resolve,
            "timestamp": incident.created_at.isoformat()
        }
        
        self.incident_history.append(incident_record)
        
        # Update pattern recognition
        if incident.type not in self.resolution_patterns:
            self.resolution_patterns[incident.type] = []
        self.resolution_patterns[incident.type].append(incident_record)
        
        # Update MTTR
        if incident.type not in self.mttr_by_type:
            self.mttr_by_type[incident.type] = []
        if incident.time_to_resolve:
            self.mttr_by_type[incident.type].append(incident.time_to_resolve)
        
        print(f"💾 Kinic: Recorded resolution for future learning")
        print(f"   Type: {incident.type}")
        print(f"   Resolution time: {incident.time_to_resolve} minutes")

# Demo: Real-Time Incident Response
def demo_incident_response():
    """
    Demonstrates how A2A coordinates incident response while Kinic
    provides historical context and learns from each incident.
    """
    print("=" * 70)
    print("DEMO: A2A + Kinic Real-Time Incident Response System")
    print("=" * 70)
    
    # Initialize systems
    coordinator = A2AIncidentCoordinator()
    memory = KinicIncidentMemory()
    
    # Register incident responders
    print("\n👥 REGISTERING INCIDENT RESPONDERS")
    print("-" * 50)
    
    responders = [
        ("ops-lead", ["database", "infrastructure", "scaling"]),
        ("security-chief", ["security", "breach", "authentication"]),
        ("senior-sre", ["kubernetes", "deployment", "monitoring"]),
        ("sre", ["logs", "metrics", "alerts"]),
        ("developer", ["api", "backend", "performance"]),
        ("junior-sre", ["documentation", "runbooks", "basic-triage"]),
        ("cto", ["executive", "decisions", "communication"]),
        ("security-analyst", ["forensics", "logs", "attack-patterns"])
    ]
    
    for responder_id, skills in responders:
        coordinator.register_responder(responder_id, skills)
    
    # Simulate incidents
    incidents = [
        Incident(
            "INC-001",
            "database-outage",
            IncidentSeverity.CRITICAL,
            ["connection timeout", "high latency", "query failures"],
            ["user-service", "order-service", "payment-gateway"]
        ),
        Incident(
            "INC-002",
            "security-breach-attempt",
            IncidentSeverity.HIGH,
            ["suspicious login attempts", "rate limit exceeded", "IP blacklist triggered"],
            ["auth-service", "user-accounts"]
        ),
        Incident(
            "INC-003",
            "api-performance",
            IncidentSeverity.MEDIUM,
            ["slow response times", "timeout errors"],
            ["public-api", "mobile-backend"]
        ),
        Incident(
            "INC-004",
            "database-outage",  # Similar to INC-001
            IncidentSeverity.CRITICAL,
            ["connection pool exhausted", "high latency", "deadlocks"],
            ["user-service", "analytics-service"]
        )
    ]
    
    print("\n\n🔥 PROCESSING INCIDENTS")
    print("-" * 50)
    
    for incident in incidents:
        # Trigger incident via A2A
        response_team = coordinator.trigger_incident(incident)
        
        # Kinic provides historical context
        print(f"\n📊 Analyzing with Kinic...")
        recommended_solution = memory.get_recommended_solution(incident)
        
        if recommended_solution:
            print(f"   ✅ Found proven solution!")
            print(f"   Estimated time: {recommended_solution.get('estimated_time', 'unknown')} minutes")
            resolution_time = recommended_solution.get('estimated_time', random.randint(10, 60))
        else:
            print(f"   ⚠️ No historical match - using standard runbook")
            resolution_time = random.randint(30, 120)
        
        # Simulate resolution
        print(f"\n⚡ Resolving incident...")
        time.sleep(1)  # Simulate work
        
        # Record resolution
        incident.status = "RESOLVED"
        incident.time_to_resolve = resolution_time
        incident.resolution_steps = [
            "Identified root cause",
            "Applied fix",
            "Verified resolution",
            "Updated monitoring"
        ]
        incident.root_cause = f"Root cause of {incident.type}"
        
        memory.record_resolution(incident)
        
        print(f"✅ Incident {incident.id} resolved in {resolution_time} minutes")
        
        # Release responders
        for responder in response_team:
            if responder in coordinator.available_responders:
                coordinator.available_responders[responder]["availability"] = "available"
                coordinator.available_responders[responder]["current_incident"] = None
        
        print("\n" + "-" * 50)
    
    # Show learning outcomes
    print("\n📈 SYSTEM LEARNING OUTCOMES")
    print("-" * 50)
    
    print(f"\nIncidents Processed: {len(memory.incident_history)}")
    
    print(f"\nMean Time To Resolve (MTTR) by Type:")
    for incident_type, times in memory.mttr_by_type.items():
        avg_time = sum(times) / len(times) if times else 0
        print(f"   • {incident_type}: {avg_time:.1f} minutes")
    
    print(f"\nResolution Patterns Learned:")
    for pattern_type, incidents in memory.resolution_patterns.items():
        print(f"   • {pattern_type}: {len(incidents)} resolutions recorded")
    
    # Demonstrate improved response
    print("\n\n🎯 DEMONSTRATION: System Has Learned")
    print("-" * 50)
    
    new_incident = Incident(
        "INC-005",
        "database-outage",
        IncidentSeverity.CRITICAL,
        ["connection timeout", "high CPU usage"],
        ["user-service"]
    )
    
    print(f"New incident: {new_incident.id} ({new_incident.type})")
    similar = memory.search_similar_incidents(new_incident)
    
    if similar:
        print(f"✨ System immediately recognizes this as similar to:")
        for s in similar[:2]:
            print(f"   • {s['incident']['id']} - resolved in {s['incident'].get('time_to_resolve', 'N/A')} min")
        
        avg_time = sum(memory.mttr_by_type.get("database-outage", [])) / len(memory.mttr_by_type.get("database-outage", [1]))
        print(f"\n🚀 Predicted resolution time: {avg_time:.1f} minutes")
        print(f"   (vs. {random.randint(60, 120)} minutes without history)")
    
    print("\n" + "=" * 70)
    print("✅ Incident Response Demo Complete")
    print("Key Achievement: A2A coordinated response while Kinic provided")
    print("historical context, reducing resolution time with each incident")
    print("=" * 70)

if __name__ == "__main__":
    demo_incident_response()