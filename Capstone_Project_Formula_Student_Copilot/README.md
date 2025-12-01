# 🏎️ Formula Student Co-Pilot (AI Agents Capstone)

**A Multi-Agent System for Engineering Team Management & Compliance**

This project is my submission for the **Google & Kaggle 5-Day AI Agents Intensive**. It demonstrates a sophisticated, agentic architecture designed to help a Formula Student team manage tasks, ensure rules compliance, and innovate on engineering designs.

---

## 🎯 Project Overview

**Track:** Enterprise Agents (Automating business/team workflows)

Formula Student is a complex engineering competition with a 190-page rulebook. Managing technical tasks, checking compliance, and brainstorming solutions is a massive cognitive load for student engineers.

The **Formula Student Co-Pilot** automates this workflow using a **Multi-Agent System**. It acts as a central hub where engineering tasks are vetted against regulations and optimized by AI before being added to the team's schedule.

### Key Features:
* **📜 Automated Compliance:** A specialized agent checks every proposed task against a structured database derived from the official **2026 Formula Student Rules** (CV Class).
* **💡 Creative Strategy:** A separate agent uses LLM reasoning to suggest compliant engineering alternatives when a design fails.
* **🛡️ Human-in-the-Loop (LRO):** Critical decisions (swapping a design) require explicit human approval via a "pause-and-resume" mechanism.
* **🧠 Long-Term Memory:** The system remembers the user's role and preferences across different sessions.
* **📝 Session State:** Manages a temporary "To-Do" list for the current engineering sprint.

---

## 🏗️ System Architecture

I implemented a **Local Sub-Agent Architecture**. This simulates a microservice pattern where specialized agents handle distinct domains, coordinated by a central manager.

```text
[ USER ]
   │ 🗣️ "Add a 6-element front wing"
   ▼
[ TEAM MANAGER AGENT ] ──────────────┐
   │                                 │ 🤝 Delegate to Sub-Agent
   │ ❌ "Non-Compliant"              ▼
   │                          [ RULES AGENT ]
   │                          (FunctionTool: Rules Database)
   │
   │ "How do we fix this?"
   ├─────────────────────────▶ [ STRATEGY AGENT ]
   │ 💡 "Try 5-elements"      (Pure LLM Reasoning)
   │
   ▼
[ HUMAN APPROVAL (LRO) ]
   │ 🛑 Pauses execution
   │ ✅ "Yes, do it."
   ▼
[ TASK DATABASE ]
   (Session State)

