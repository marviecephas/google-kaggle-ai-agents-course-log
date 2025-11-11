# 5-Day AI Agents Intensive: Day 1 - Introduction to Agents

This folder contains my completed codelabs and practice tasks for Day 1 of the Google & Kaggle 5-Day AI Agents Intensive.

## 🚀 Official Day 1 Concepts

* **Core Agent Components:** The fundamental parts of an agent (Model, Tools, Orchestrator, Memory).
* **Agent Development Kit (ADK):** Using the ADK to build a basic agent.
* **Multi-Agent Systems:** Using a `SequentialAgent` to chain multiple agents together (`ResearcherAgent` -> `SummarizerAgent`).

---

## 🛠️ Extra Practice Tasks & Key Learnings

Beyond the main codelabs, I set two practice tasks for myself to better understand the ADK.

### Task 1: Adding a Custom `calculator_tool`

I built a simple `calculator_tool` and added it to the Day 1 agent. This led to a major learning experience.

* **The Problem:** When I ran the agent with a prompt like "What is 2 + 2?", the agent's "brain" (LLM) correctly decided to use the `calculator_tool`. However, the API consistently returned a `ClientError: 400 INVALID_ARGUMENT... Tool use with function calling is unsupported`.
* **The Lesson:** This was a critical lesson in **model compatibility**. The model we were using (`gemini-flash-latest`) did not support the specific "tool use" feature the ADK was trying to call. This proved that an agent's architecture is useless if the underlying model doesn't support its features.

### Task 2: Building a 3-Agent Sequential Chain

I extended the Codelab 2 multi-agent system by adding a `TranslatorAgent` to the end of the chain:
`ResearcherAgent` $\rightarrow$ `SummarizerAgent` $\rightarrow$ `TranslatorAgent`

* **The Problem:** On my first try, my `ResearcherAgent` saw the word "French" in the prompt and decided to do the research *and* the translation. This "prompt bleeding" confused the other agents and broke the chain's logic.
* **The Fix:** I re-wrote the instructions for each agent to be **single-purpose** and "dumber" (e.g., "Your ONLY job is to find information... Ignore any requests for translation."). This fixed the chain completely.
* **The Lesson:** **Strict prompt engineering** is non-negotiable for multi-agent systems. You must force each agent to stay in its own lane to get a predictable, reliable result.

### 📓 View My Work

* [See the notebook with my practice tasks here.](./notebook1c009fb213.ipynb%20(3).txt)
