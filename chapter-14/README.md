# Chapter 14 — Safety, Security, and Responsible Agentic AI

This chapter's lab is about attacking and then defending an agent.
Agents do not just talk, they act — so a bug here can delete data or
leak secrets, not just say something wrong. The code in this folder is
the worked example: a 3-layer defense (system-prompt hardening, input
validation, output filtering) plus a read-only guard for the SQL tool,
all built for a small customer-support agent.

## Files

- `01_defense_in_depth.py` — all three layers from the book's worked
  example in one runnable file: the hardened `SYSTEM` prompt, the
  `safe_user_input` regex-plus-LLM validator, the `safe_output` PII
  redactor (Aadhaar/PAN patterns), and a read-only `run_sql` guard for
  the MCP server side. The book's `small_llm.classify(...)` call is
  illustrative pseudocode (no such model is defined in the chapter),
  so this file stubs it with a function that always returns "benign" —
  swap it for a real guardrail model (e.g. Llama Guard 2) in
  production.
- `requirements.txt` — notes that no third-party packages are needed
  to run the demo as shipped.

## How to run

1. No virtual environment or API key is strictly required — the demo
   only uses the Python standard library. If you want to isolate it
   anyway:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   ```

2. Run the script:

   ```bash
   python 01_defense_in_depth.py
   ```

## What to expect

The script prints the hardened system prompt, then runs three sample
user inputs through `safe_user_input`. The first (a normal question) is
allowed. The second ("ignore all previous instructions...") is blocked
by the regex blocklist. The third (a SQL injection attempt) is also
blocked by the regex blocklist. It then shows `safe_output` redacting a
fake PAN and Aadhaar number, and confirms `run_sql` rejects a `DELETE`
statement with a `PermissionError`.

## Using this for the Chapter 14 lab

The book's Lab 14 ("Red-team your Chapter 13 MCP agent") asks you to
attack the SQLite agent from `chapter-13/07_sqlite_agent.py` with
direct injection, indirect injection (via a poisoned database row), and
an excessive-agency request (asking the agent to delete rows). Then you
re-run those attacks after adding the mitigations in this file:

1. Paste `SYSTEM` from `01_defense_in_depth.py` into the agent's system
   message before creating the ReAct agent in `07_sqlite_agent.py`.
2. Run each user message through `safe_user_input` before sending it to
   the agent; reject it if `ok` is `False`.
3. Make sure `chapter-13/05_sqlite_server.py`'s `query` tool still only
   allows `SELECT` (it already does) — this is the same idea as the
   `run_sql` guard here, applied inside the MCP server itself.

Compare which attacks succeed before and after, and write up the
2-page report the lab asks for.
