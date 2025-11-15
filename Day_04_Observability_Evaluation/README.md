# 5-Day AI Agents Intensive: Day 04 - Observability & Evaluation

This folder contains my work for Day 4. This unit was all about **checking our agent's quality** and proving that it works.

This was a two-part lesson:
1.  **Observability (4a):** How to watch our agent's "thoughts" to find and debug problems *manually*.
2.  **Evaluation (4b):** How to build *automated tests* to catch bugs and prevent them from returning (also called "regression testing").

### 📓 View My Work

* **[Codelab 4a: Agent Observability](./day-4a-agent-observability.ipynb.txt)**
* **[Codelab 4b: Agent Evaluation](./day-4b-agent-evaluation.ipynb.txt)**
* **[My Practice Task: The "Buggy" Shopping Agent](./shopping-agent/)** (This folder contains my `agent.py` and evaluation files)

---

## 📚 Key Concepts from Codelab 4a (Observability)

* **`adk web --log_level DEBUG`**: The most important command for interactive, manual debugging. It launches a web UI where you can chat with your agent and see a complete **Trace** of its "thoughts" (which tools it called, what data it passed).
* **`LoggingPlugin`**: This is the "production" version of logging. It's a built-in plugin you add to your `Runner` to automatically capture all agent activity (LLM requests, tool calls, errors) into a log file.
* **Callbacks vs. Plugins**: A **Callback** is a *single hook* (like `before_agent_callback`) that lets you run code at a specific moment. A **Plugin** is a *class* that groups these callbacks to perform a full job (like the `LoggingPlugin` does). You don't need to write your own callbacks if you use a built-in plugin.

---

## 📚 Key Concepts from Codelab 4b (Evaluation)

* **`adk eval`**: The main command-line tool to run an automated test suite against your agent.
* **`*.evalset.json`**: This is the "golden test" file. You write a perfect, ideal conversation in this file, including every user prompt, every tool the agent *should* call, and the perfect final answer.
* **`test_config.json`**: This is the "rules" file. You set the pass/fail thresholds here (e.g., `response_match_score: 1.0` to require a perfect text match).
* **LLM-as-Judge**: For advanced tests, you can change the criteria to `hallucinations_v1` or `safety_v1` and set an `evaluator_model_name`. This tells the ADK to use *another AI* to judge your agent's quality instead of just comparing text.

---

## 🛠️ My Practice Task: Debugging & Locking the `shopping-agent`

I combined both of today's lessons into a single practice task.

### 1. The Goal
I built a `shopping-agent` with tools to add items (`Notes`) and count them (`get_item_count`).

### 2. The Bug
I intentionally made the agent's prompt and tools confusing. When I ran it, the agent failed in a very strange way.

### 3. Using Observability (4a) to Find the Bug
I couldn't figure out why the agent was failing, so I used the `LoggingPlugin` to get a full trace. The logs showed the bug perfectly!
1.  The agent's "brain" (LLM) got confused.
2.  It skipped the `view_list` step.
3.  It called my `get_item_count` tool directly but passed the wrong argument: `Arguments: {'item_list': 'shopping list'}`.
4.  My buggy tool (which was expecting a list) ran `len('shopping list')`.
5.  The agent confidently (and incorrectly) reported: **"There are 13 items on your shopping list."**

### 4. Using Evaluation (4b) to Fix the Bug
After I saw the log, I knew how to fix it:
1.  I fixed my `get_item_count` tool to require a `List[str]`.
2.  I fixed the agent's instructions to be more precise.
3.  I created a "golden test" file (`shopping_test.evalset.json`) that describes the *perfect* conversation, including the correct tool calls (`view_list`, then `get_item_count`) and the correct final answer (`"You have 3 items on your list."`).
4.  I created a `test_config.json` to require a 100% perfect score.

Now, I can just run `!adk eval` anytime. This automated test will instantly **FAIL** if any future change breaks my agent's counting logic, which "locks in" my fix and prevents future f
