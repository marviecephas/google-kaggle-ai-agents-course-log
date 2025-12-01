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

```
## 🤖 The Agents

The system is composed of three specialized agents working in a hierarchy:

### 1. Team Manager Agent (The Boss)
* **Role:** Central Orchestrator.
* **Responsibility:** Manages the user interaction, delegates tasks to specialists, and handles state.
* **Logic:** It follows a strict **Chain-of-Thought** prompt to ensure it never skips a step (e.g., "Step 1: Check Rules. Step 2: If failed, ask Strategy...").

### 2. Rules Agent (The Lawyer)
* **Role:** Compliance Officer.
* **Responsibility:** Checks proposed engineering tasks against the 2026 Formula Student Rulebook.
* **Tooling:** Equipped with a custom `FunctionTool` (`get_rules_from_db`) that queries a structured Python dictionary of key regulations (Powertrain, Chassis, Aero, etc.). This ensures strict adherence to facts and prevents hallucination.

### 3. Strategy Agent (The Engineer)
* **Role:** Creative Problem Solver.
* **Responsibility:** Proposes valid engineering alternatives when a design fails compliance.
* **Logic:** It relies on the LLM's internal knowledge of physics and engineering principles to "invent" a solution that meets the user's goal without breaking the rules identified by the Rules Agent.

---

## 🛠️ Technical Implementation

This project uses the **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash Lite**.

### Key Concepts Demonstrated:
1.  **Function Tools:** * `get_rules_from_db`: Simulates a vector database lookup for regulations.
    * `add_team_task`: Manages the session-specific task list.
    * `view_team_tasks`: Retrieves the current state.
2.  **Long-Running Operations (Human-in-the-Loop):** * Implemented a critical safety gate using `tool_context.request_confirmation()`. 
    * When the Strategy Agent suggests a major design change, the system **PAUSES** execution. It waits for the human user to explicitly approve or reject the change before writing it to the database.
3.  **Memory Management:**
    * **Session State:** Used `tool_context.state` as a temporary "scratchpad" for the current engineering sprint's task list.
    * **Long-Term Memory:** Utilized `MemoryService` and `preload_memory` to persist user context (e.g., "User is Marvellous, the Team Lead") across different sessions, creating a personalized experience.

---

## 🚀 How to Run

1.  **Clone the Repository**
    ```bash
    git clone [YOUR_REPO_LINK]
    cd formula-student-copilot
    ```

2.  **Install Dependencies**
    ```bash
    pip install google-adk
    ```

3.  **Set API Key**
    Ensure your Google Cloud/AI Studio API Key is set in your environment:
    ```bash
    export GOOGLE_API_KEY="your_key_here"
    ```

4.  **Run the Agent**
    You can run the agent interactively using the provided Python script or notebook. Since this uses a **Local Sub-Agent** architecture, no separate servers or ports are required.
    ```python
    # Example usage
    from formula_student_copilot.agent import runner
    import asyncio

    await runner.run_debug("We want to design a 6-element front wing.")
    ```

---

## 🎥 Verification & Demo

I verified the system through **interactive end-to-end runs** to demonstrate the correct multi-agent behavior:

### The "Golden Path" Demo Scenario
1.  **Input:** "We want to design a 6-element front wing."
2.  **Rules Agent (Logic Check):** Correctly identified this violates the "Max 5 elements" rule.
3.  **Strategy Agent (Reasoning):** Correctly reasoned that a 5-element wing is the compliant alternative.
4.  **Team Manager (LRO):** Correctly **PAUSED** execution to ask for my approval before saving the task.
5.  **Outcome:** After I approved, the task was saved to the Session State.

---

### 👨‍💻 Author
**Marvellous**
*Aspiring ML/AI/Robotics Engineer & Formula Student*
