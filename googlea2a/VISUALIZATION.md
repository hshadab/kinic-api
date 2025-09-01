# Kinic × Google A2A Protocol Visualization

A **ready-to-run interactive UI** for visualizing agent-to-agent communication in real-time.

## Features

* **Translucent (glassmorphism) agent cards** with live stats (RPS, p95 latency, RAG hits/min)
* **Animated A2A links** (glowing edges with arrowheads)
* **Real-time pulses** traveling along links for **messages / tasks / artifacts**
* **Force / Ring / Grid** layouts, **drag**, **zoom/pan**, **dark/light** toggle
* **WebSocket connector** for **live A2A events** (or use built-in **Demo** traffic)
* **Inspector panel** with click-to-inspect and a live event log
* **PNG export** of the current topology

## Quick Start

Simply open `index.html` in a modern browser, or serve the folder with any static server.

**Live Demo**: https://hshadab.github.io/kinic-api/googlea2a/

---

## What You'll See

* **Kinic AI Memory** sits at the center (special teal/green accent with gradient effects)
* Agents like **Planner**, **Researcher**, **Reviewer**, **Toolsmith**, **Concierge** are connected to Kinic and each other via **A2A** links
* Click a card to view details; watch **pulses** animate from source → target when messages/tasks/artifacts flow
* Each agent has unique gradient colors for easy identification

---

## Understanding the Visualization

### What It Shows

**Big picture:** a live "map" of collaborating agents where:

* **Cards = agents** (Planner, Researcher, Reviewer, Toolsmith, Concierge, etc.)
  * The **Kinic** card is styled distinctly because it represents **shared semantic memory** that multiple agents consult
* **Lines with arrowheads = A2A links** (agent-to-agent protocol connections)
* **Glowing dots ("pulses") moving along a line = live traffic**:
  * **Blue** pulse → a **Message**
  * **Purple** pulse → a **Task**
  * **Green** pulse → an **Artifact** (e.g., a reference or file)

Think of it as a network monitor for your agent ecosystem: who's talking to whom, using which A2A construct, right now.

```
[Planner] →→→ (blue/purple/green pulses) →→→ [Kinic AI Memory]
     │                                          ▲
     ├─────────→ [Researcher] ────────────────┘ │
     └─────────→ [Reviewer]                     │
```

---

## Purpose

1. **Explain & demo A2A quickly.** Show how agents discover each other and collaborate through **messages**, **tasks**, and **artifacts**—with **Kinic** acting as shared memory
2. **Observe live behavior.** When connected to a WebSocket feed, you see **real traffic** flowing across edges in near real-time
3. **Debug and validate.** Use the Inspector log to confirm you're issuing the right events, that links appear as expected, and that latency assumptions look sensible
4. **Onboard non-developers.** The interface turns protocol flows into a simple, visual story for PMs, partners, and execs

---

## How to Read the UI

### 1) Top Bar (Controls)

* **Connect**: Attach to a `ws://` / `wss://` endpoint that emits A2A-style events
* **Demo**: Toggles built-in simulated traffic (helpful when you don't have a live feed)
* **Layout**: 
  * **Ring** (default) - cleanly spaces agents in a circle around Kinic
  * **Force** - lets agents settle dynamically
  * **Grid** - tidies for screenshots
* **Pause/Resume**: Freezes the physics (useful for reading or presenting)
* **Reset View**: Returns to default zoom and position
* **Dark/Light toggle**: Theme preference

### 2) Stage

* **SVG edges** between agents show **direction** (arrowheads)
* **Pulses** animate along an edge to indicate a live event in flight; speed roughly reflects the provided `latencyMs`
* **Drag a card** to pin or reposition it; zoom/pan with mouse or trackpad

### 3) Agent Cards

Each translucent "glass" card shows:

* **Name & role** (e.g., "Researcher — Web + RAG")
* **Unique gradient colors** for each agent type
* **Metrics** (live, illustrative by default):
  * **RPS**: Rough request rate observed for that agent (increments on events)
  * **p95**: Rolling **latency** estimate in ms (from each event's `latencyMs`)
  * **RAG**: Increments when events **target Kinic**, hinting at memory lookups/updates

> Tip: Click a card to **focus** it and view details in the **Inspector**.

### 4) Legend

Color keys for pulses (Message/Task/Artifact) and the meaning of the A2A edge.

### 5) Inspector (Right Panel)

* **Agent details** for the currently selected card
* **Event log** showing a running list of recent events (keeps a rolling window so it doesn't grow unbounded)

### 6) Footer

* **Export PNG** captures the current view (useful for reports or PRDs)

---

## Hooking Up Live A2A Data

Click **Connect** and point to a WebSocket (e.g., your A2A Inspector proxy or broker). The app expects JSON events like:

```json
{
  "type": "task",
  "source": "planner",
  "target": "kinic",
  "latencyMs": 132,
  "payload": {"note": "optional"}
}
```

### Event Format

* `type`: `"msg" | "task" | "artifact"`
* `source` / `target`: Agent IDs (new ones are auto-created)
* `latencyMs`: Drives pulse speed and metrics
* `payload`: Optional, ignored by the visualizer but you can surface it in the inspector if needed

Unknown agents/links are **created on the fly** so you can stream any topology without preconfiguring it.

Use **Demo** to toggle built-in simulated traffic if you don't have a live feed yet.

---

## Architecture at a Glance

* **Edges & pulses** are SVG (`<path>` with arrowheads). Pulses are small circles that **animate along the path** using `getPointAtLength()` in `requestAnimationFrame`
* **Agent cards** are **HTML** (glassmorphism) **positioned over the SVG**, kept in sync with the force simulation and the current zoom transform
* **Layouts**:
  * **Force** - Collision + link strength tuned to highlight Kinic
  * **Ring** - Kinic at center, others arranged in a circle
  * **Grid** - Tidy comparison view

---

## Why Kinic is Central

Kinic is highlighted because it represents **persistent, shared memory**—a substrate that multiple agents use for:

* **Saving** conversation context or artifacts (e.g., research snippets)
* **Searching** for prior knowledge (semantic retrieval)
* **Sharing** references via A2A **artifacts** so other agents can reproduce or validate the context

In many real systems, Kinic (or a memory service) becomes the "hub" that keeps work coherent across different agent roles, teams, and even runtimes.

---

## Typical Use Cases

* **Live demo** of an A2A "team": planner → researcher → reviewer, all reading/writing Kinic
* **Integration testing**: As you bring up an A2A Memory Broker or Tooling Agent, watch edges appear and pulses flow to validate the wiring
* **Performance spot-checks**: Sanity-check latencies in context (are Kinic lookups fast? which agent is slow?)
* **Explaining tasks vs. messages vs. artifacts** to stakeholders with a clear, visual aid

---

## Design Choices

* **Translucent cards & neon edges** → High visual contrast, easy to read in demos
* **Ring on load** → Prevents initial card pile-ups; you can switch to **Force** to let it "breathe"
* **Directional edges** → Highlights who initiates vs. who serves
* **Color-coded pulses** → Quick mental map of A2A constructs without reading logs
* **Unique gradient colors per agent** → Each agent has a distinct visual identity inspired by Kinic's brand

---

## Customization

### Make It Yours

* Add/rename agents and links in `seedAgents` / `seedLinks` (in the JavaScript section)
* Customize the look via CSS variables for colors, translucency, glow
* Modify agent colors and gradients for your brand

### Agent Colors

Each agent type has unique gradient colors:
* **Kinic**: Teal to cyan gradient (#4ef6b2 → #6dd3ff)
* **Planner**: Blue to purple
* **Researcher**: Purple to pink
* **Reviewer**: Orange to pink
* **Toolsmith**: Light blue to lavender
* **Concierge**: Yellow to orange

---

## Next Enhancements (Easy to Add)

* **Task vs Message modes** per edge (thicker line for tasks, dashed for messages)
* **Agent Card metadata** (capabilities/extensions) inside the right-hand inspector
* **Packet loss / retry** visual cues if your stream emits those events
* **Group nodes** by team/workspace with soft, translucent "blobs"
* **Render payloads** in the Inspector (e.g., show Task state updates, artifact URIs)
* **Edge semantics**: Labeled skills ("memory.search", "memory.save")
* **Health overlays**: Colorize edges or cards based on error rate / saturation
* **Filtering**: Show only a subset of agents or event types for dense topologies

---

## Kinic/A2A-Aware Touches

* **A2A edges** are labeled and animated; pulses are color-coded:
  * **Message** (blue), **Task** (purple), **Artifact** (green)
* **Kinic** card gets a distinct ring and accent, signaling its **shared memory** role
* The **Inspector** is intentionally minimal but wired so you can expand it with A2A task/message details, Agent Cards, or Memory artifacts later

---

## Limitations to Be Aware Of

* It's a **front-end visualizer**: No A2A handshake or schema validation on its own
* Metrics are **illustrative** unless your feed emits precise rates—latency is derived from each event's `latencyMs`
* Physics is optimized for **small to medium** graphs (dozens of agents), not hundreds

---

## One-Liner Summary

**Kinic × Google A2A Protocol** is a lightweight, live network map for agent collaboration: it turns A2A messages, tasks, and artifacts into animated flows between translucent agent cards—with **Kinic** as shared memory—so you can **explain**, **debug**, and **demo** your multi-agent system in seconds.

---

## Technical Details

### Browser Compatibility
- Modern browsers with ES6 support
- Chrome, Firefox, Safari, Edge (latest versions)
- WebSocket support required for live connections

### Performance
- Optimized for 5-50 agents
- 60fps animations with requestAnimationFrame
- Efficient SVG path animations for pulses

### File Structure
- Single HTML file with embedded CSS and JavaScript
- No build process or dependencies required
- Fully self-contained visualization

---

## License

Part of the Kinic project. See main repository for license details.