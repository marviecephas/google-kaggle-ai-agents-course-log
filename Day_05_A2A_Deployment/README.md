# 5-Day AI Agents Intensive: Day 05 - A2A & Deployment

This folder contains my work for the final day, which covered the two most advanced, production-level concepts: how to make agents communicate with each other (A2A) and how to deploy them to the cloud.

### 📓 View My Work

* **[Codelab 5a: Agent2Agent Communication](./day-5a-agent2agent-communication.ipynb.txt)**
* **[Codelab 5b: Agent Deployment (Conceptual)](./day-5b-agent-deployment.ipynb.txt)**

---

## 📚 Key Concepts from Codelab 5a (Agent-2-Agent)

This was the most exciting concept: building a multi-agent system where agents are not just in the same file but are completely separate applications (microservices) that talk over the internet.

* **What is A2A?** The "Agent-2-Agent" (A2A) protocol is a standard "language" that lets different agents, even ones written by different companies or in different programming languages (like Python and Java), communicate and delegate tasks.

* **The Analogy:** I learned to think of it as a "Head Chef" and a "Bakery":
    * **Exposing an Agent (The "Bakery"):** This is the agent you want to share. You use the `to_a2a(agent)` function to wrap your agent in a web server. This also automatically publishes an "agent card" (a JSON file) that acts as the agent's public "menu."
    * **Consuming an Agent (The "Head Chef"):** This is your main agent. You use the `RemoteA2aAgent(agent_card="...")` class to "dial the phone" to the bakery. You just point it at the bakery's "agent card" URL, and it learns the "menu."

* **Tools vs. Sub-Agents (My "Aha!" Moment):**
    * **`tools=[...]`**: You give your agent a "dumb" tool, like a *knife*. The agent's main brain must do all the thinking for *how* to use the knife.
    * **`sub_agents=[...]`**: You give your agent a "smart" assistant, like a *Pastry Chef*. The Head Chef (main agent) doesn't tell the Pastry Chef *how* to make a cake; it just **delegates** the entire complex task. This is what you do with a `RemoteA2aAgent`—you delegate the "product lookup" task to the specialist agent.

---

## 📚 Key Concepts from Codelab 5b (Deployment)

This notebook required a Google Cloud account, which I couldn't use. However, I was still able to learn the *conceptual process* of taking an agent from a local notebook to a real, scalable product.

### 1. How to "Package" an Agent for Deployment

A production-ready agent isn't a single `.ipynb` file. It's a professional folder structure containing four key files:
* **`agent.py`**: The agent's logic.
* **`requirements.txt`**: The list of Python libraries the server needs to install (e.g., `google-adk`).
* **`.env`**: An environment file to tell the agent it's in the cloud (e.g., `GOOGLE_GENAI_USE_VERTEXAI=1`).
* **`.agent_engine_config.json`**: The hardware settings, like how much CPU and RAM to use.

### 2. The "Real" Version of Memory
In Day 3, we used `InMemoryMemoryService` (temporary) and `DatabaseSessionService` (persistent, but simple). This codelab introduced the production-level solution: **Vertex AI Memory Bank**. This is a fully managed cloud service that provides permanent, intelligent, and shareable long-term memory for all your agents.

### 3. The "Deploy" Button
The ADK makes deployment simple with one command:
`!adk deploy agent_engine ... sample_agent`

This command takes your "package" folder and handles all the complex cloud setup for you.

### 4. How to Test a "Live" Agent
Once an agent is deployed, you don't use `InMemoryRunner`. Instead, you use the official Python SDK to call your agent over the internet, just as a real application would:
`remote_agent.async_stream_query(message="...")`

---

## 🎓 Next Step: The Capstone Project!

I will be applying all concepts from these 5 days to my "Formula Student Co-Pilot" project.
