# 5-Day AI Agents Intensive: Day 2 - Agent Tools & Interoperability

[cite_start]This folder contains my work for Day 2[cite: 86]. This unit was a deep dive into two of the most powerful, production-ready patterns for building advanced agents: **Model Context Protocol (MCP)** and **Long-Running Operations (LROs)**.

### 📓 View My Work

* **[See the completed Day 2 Codelab here.](./day-2b-agent-tools-best-practices.ipynb)**

---

## 🚀 Key Concepts Learned

### 1. Model Context Protocol (MCP)

This is how an agent can use pre-built tools from external services without you having to write the integration code.

* [cite_start]**What it is:** A standard "protocol" that lets your agent (a "client") connect to an "MCP server" (a "tool store")[cite: 106].
* [cite_start]**How I used it:** I used the `McpToolset` to connect to a test server (`@modelcontextprotocol/server-everything`)[cite: 111, 113]. [cite_start]This instantly gave my agent a new skill, the `getTinyImage` tool, which I used to generate an image from a simple prompt[cite: 119].

### 2. Long-Running Operations (LROs) / Human-in-the-Loop

This is the most critical concept for building safe, trustworthy agents. [cite_start]I learned how to build a tool that can **pause** its work, **ask for human approval**, and then **resume** after the human gives an answer[cite: 126].

[cite_start]This is essential for any real-world task involving money, deleting data, or high-cost operations[cite: 175].

#### How it Works:

This pattern requires two parts working together:

**A. The "Pausable" Tool (e.g., `place_shipping_order`):**
* [cite_start]It uses a special `ToolContext` argument given to it by the ADK[cite: 128].
* It checks for approval: `if not tool_context.tool_confirmation:`.
* [cite_start]It pauses the agent by calling: `tool_context.request_confirmation(...)`[cite: 128].
* [cite_start]It resumes by checking the human's answer: `if tool_context.tool_confirmation.confirmed:`[cite: 134].

**B. The "Resumable" App (The "Manager"):**
* You must wrap the agent in an `App` with `ResumabilityConfig(is_resumable=True)`. [cite_start]This makes the agent "stateful" so it can remember being paused[cite: 140, 141].
* The main workflow code (like `run_shipping_workflow`) then manages the entire process:
    1.  **Runs** the agent.
    2.  [cite_start]**Detects** the pause by checking the events for `adk_request_confirmation`[cite: 147].
    3.  [cite_start]**Resumes** the agent by calling `run_async()` a *second time*, passing in the human's decision and the original `invocation_id`[cite: 149, 160].
