# Chapter 13 — Model Context Protocol and Interoperability

This chapter's lab is about the Model Context Protocol (MCP): a small,
shared way for an AI app to ask another process for tools, data, or
prompts. The code here builds three MCP servers of growing complexity
(echo, weather, then a SQLite database) and the LangGraph agents that
talk to them. Each server is a separate process; the client launches it
over stdio and treats its tools like any other LangChain tool.

## Files

- `01_echo_server.py` — the smallest possible MCP server. One tool,
  `echo`, that returns the input text unchanged.
- `02_echo_agent.py` — a LangGraph ReAct agent that launches
  `01_echo_server.py` as a subprocess and calls its `echo` tool.
- `03_weather_server.py` — the worked-example server. One tool,
  `get_weather`, backed by a fake in-memory table of three Indian
  cities.
- `04_weather_agent.py` — the worked-example client. Asks "Should I
  carry an umbrella in Bengaluru today?" and lets the agent call
  `get_weather`.
- `05_sqlite_server.py` — Lab 13.1's server. Exposes a SQLite database
  through three tools: `list_tables`, `describe`, and `query`
  (SELECT-only).
- `06_seed_db.py` — a setup helper (not printed in the book) that
  creates `shop.db` with 20 customers and 200 orders, as the lab
  instructions describe. Run this once before the SQLite lab.
- `07_sqlite_agent.py` — Lab 13.1's client. Same pattern as
  `04_weather_agent.py`, pointed at `05_sqlite_server.py`, asking
  "Which 5 customers spent the most last month?"
- `requirements.txt` — packages needed for this chapter's labs, pinned
  the way the book pins them.

## How to run

1. Create and activate a virtual environment, then install packages:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Export your Anthropic API key (the servers themselves need no key —
   only the LangGraph client scripts call an LLM):

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. Run the echo example. You do not start the server by hand — the
   client launches it as a subprocess:

   ```bash
   python 02_echo_agent.py
   ```

4. Run the weather example the same way:

   ```bash
   python 04_weather_agent.py
   ```

5. Run the SQLite lab. Seed the database first, then run the client:

   ```bash
   python 06_seed_db.py
   python 07_sqlite_agent.py
   ```

## What to expect

`02_echo_agent.py` prints the word "hello" (or a sentence containing
it) after the agent calls the `echo` tool.

`04_weather_agent.py` prints a short recommendation to carry an
umbrella, based on the fake "light rain" reading for Bengaluru.

`07_sqlite_agent.py` prints a natural-language answer listing the top
5 spenders. Behind the scenes the agent calls `list_tables`, then
`describe(table="orders")`, then a `SELECT` query — trace this in
LangSmith if you have Chapter 12's tracing set up.

## Security note

Chapter 14's lab attacks and defends the SQLite agent built here. The
`query` tool already rejects non-`SELECT` statements — that is a
deliberate first line of defense, not an oversight.
