# 5-Day AI Agents Intensive: Day 03 - State, Sessions, and Memory

This folder contains my work for Day 3. This was the most important day so far, as we learned how to make our agents **stateful** (able to remember information).

We covered two types of memory:
1.  **Session State:** A temporary "scratchpad" for a *single* conversation (e.g., a shopping list).
2.  **Long-Term Memory:** A permanent, searchable database of facts that persists *across multiple* conversations (e.g., user preferences).

### 📓 View My Work

* **[Codelab 3a: Agent Sessions](./day-3a-agent-sessions.ipynb.txt)**
* **[Codelab 3b: Agent Memory](./day-3b-agent-memory.ipynb.txt)**
* **[My Practice Task: "Smart Assistant"](./notebook30a6a25f29.ipynb.txt)**

---

## 📚 Key Concepts from Official Codelabs

### Codelab 3a: Agent Sessions

* **`SessionService`**: This is the "filing cabinet" that manages conversations.
* **`InMemorySessionService`**: Temporary storage for sessions. [cite_start]All memory is lost when the notebook restarts[cite: 42].
* **`DatabaseSessionService`**: Persistent storage using a database (like SQLite). [cite_start]This allows a user to restart an application and resume a conversation[cite: 47, 48, 54].
* [cite_start]**`Session.State`**: This is the agent's "scratchpad" for the *current* conversation[cite: 32, 33]. It's a key-value store perfect for temporary info.
* [cite_start]**`Context Compaction`**: An automatic process to summarize a long chat history[cite: 68]. This saves tokens, reduces cost, and keeps the agent focused.

### Codelab 3b: Agent Memory

* [cite_start]**`MemoryService`**: This is the "long-term knowledge base" that stores facts across *all* sessions[cite: 181].
* [cite_start]**`add_session_to_memory()`**: The function to manually save a session's important facts to the long-term memory[cite: 211, 224].
* **`load_memory` vs. `preload_memory`**: These are the two tools an agent can use to *retrieve* long-term memory.
    * [cite_start]**`load_memory` (Reactive):** The agent decides when to search its memory[cite: 227]. [cite_start]The risk is that it might "forget" to look[cite: 227].
    * [cite_start]**`preload_memory` (Proactive):** Automatically searches memory before *every* turn[cite: 227].
* **Callbacks (`after_agent_callback`)**: This is the key to automation. [cite_start]By attaching a function here, we can make the agent automatically save its memory after every single turn[cite: 253, 256].

---

## 🛠️ My Practice Task: "Smart Assistant"

I combined all of today's concepts into a single "Smart Assistant" agent to prove I understood the difference between the two memory types.

### The Goal

Build an agent that could:
1.  Manage a **temporary shopping list** using `Session.State`.
2.  Remember **permanent user facts** (like a favorite snack) using `MemoryService`.
3.  Do all this automatically using `DatabaseSessionService`, `preload_memory`, and the `auto_save_to_memory` callback.

### What I Built

* [cite_start]**Tools:** I created `add_to_shopping_list` [cite: 304][cite_start], `remove_item` [cite: 304-305][cite_start], and `view_shopping_list`[cite: 305], which all use `tool_context.state` to manage the temporary list.
* [cite_start]**Agent:** The agent was given my custom tools *and* the `preload_memory` tool[cite: 312].
* [cite_start]**Automation:** I used the `auto_save_to_memory` callback [cite: 312] [cite_start]and the `DatabaseSessionService` [cite: 313] to make all memory persistent and automatic.

### Key Learnings (From My Test Results)

* **SUCCESS (Session State):** The `Session.State` tools worked perfectly. [cite_start]In `session_two`, the agent successfully used the `add_to_shopping_list` tool twice, responding, "Okay, I've added milk" and "Okay, I've added eggs"[cite: 318, 319].
* [cite_start]**LEARNING (Long-Term Memory):** In that same session, when I asked, "What is my favorite snack?", the agent correctly replied, "I'm sorry, I can't help you with that"[cite: 321]. This proves the system works! The `preload_memory` tool ran, searched the empty long-term memory, found nothing, and the agent correctly followed its instructions *not* to hallucinate an answer.
* [cite_start]**REAL-WORLD ERROR (API Failure):** My final test in `session_three` failed with a `ServerError: 503 UNAVAILABLE`[cite: 344]. [cite_start]This means the model was overloaded[cite: 345]. This was a great real-world lesson showing that agents must be built to handle unexpected API failures.
