# Chapter 10 — Persistence, Checkpointing, and Human-in-the-Loop

This chapter teaches how to make LangGraph agents durable. A
checkpointer saves a snapshot of the graph's state after every
super-step, so agents can survive crashes, pause for human approval,
and support time travel. The main lab builds a human-in-the-loop
travel-booking agent that searches flights, drafts a proposal, pauses
for approval, and books the flight once a human says "yes" — all
backed by `SqliteSaver` so progress survives a restart.

## Files

| File | What it shows |
|---|---|
| `01_checkpointers.py` | The three checkpointer flavours: `InMemorySaver`, `SqliteSaver`, `PostgresSaver`. Postgres connection string comes from `POSTGRES_CONN_STRING`. |
| `02_minimal_persistent_graph.py` | The smallest persistent graph: a two-node counter that keeps counting across repeated `invoke()` calls on the same thread. |
| `03_interrupts_and_resume.py` | Dynamic interrupts (`interrupt(...)` inside a node) and resuming a paused graph with `Command(resume=...)`. |
| `04_time_travel.py` | Listing checkpoint history with `get_state_history`, pinning a checkpoint, editing state, and forking a new branch. |
| `05_encrypted_serializer.py` | Wrapping a checkpointer with `EncryptedSerializer` so sensitive state is not stored in plaintext. Needs `LG_ENCRYPTION_KEY`. |
| `06_durable_research_agent.py` | The chapter's worked example: a slow three-node research agent that resumes correctly after a crash. |
| `07_solved_problem_refund_approval.py` | Solved Problem 10.2: a refund agent that only pauses for manager approval above INR 10,000. |
| `08_lab_travel_booking_agent.py` | **The chapter lab.** HITL travel-booking agent: search, draft, pause for approval, book. |

## How to run

No LLM API keys are needed — every example uses stub functions for
"real" work (flight search, payments API, etc.), exactly as in the
book.

Install what these files need:

```bash
pip install langgraph langgraph-checkpoint-sqlite
# Only if you try the Postgres example:
pip install langgraph-checkpoint-postgres
```

Environment variables used by some files (never hardcode these):

- `POSTGRES_CONN_STRING` — for `01_checkpointers.py`'s Postgres example.
- `LG_ENCRYPTION_KEY` — a base64-encoded 32-byte AES key, for `05_encrypted_serializer.py`.

Run any file directly, for example:

```bash
python 02_minimal_persistent_graph.py
python 08_lab_travel_booking_agent.py
```

Each script writes its own SQLite file (`counter.db`, `travel.db`,
`research.db`, `refunds.db`) in the current folder. Delete a `.db`
file if you want to start a script's thread fresh instead of resuming.
