# Chapter 1 — Introduction to Agentic AI

This chapter's lab (Lab 1: Your First Mini-Agent in Python) gets your
toolchain working, makes your first LLM call, and turns that call into
a tiny one-shot agent. The agent reads a message, asks the LLM to pick
one of two actions (`greet` or `compute`), and then runs that action
in plain Python. The LLM never does the math itself — it only chooses
the tool and the argument. That is the smallest agent you can build.

## Files

- `hello_llm.py` — the simplest possible LLM call. Prints a one-sentence
  answer to "what is an AI agent?".
- `mini_agent.py` — the one-shot mini-agent. Routes a user message to
  either `greet()` or `compute()` using a single LLM call as the router.
- `requirements.txt` — packages needed for this chapter's labs.

## How to run

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Get an API key from `console.anthropic.com` and export it:

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. Run each script:

   ```bash
   python hello_llm.py
   python mini_agent.py
   ```

## What to expect

`hello_llm.py` prints one sentence explaining what an AI agent is.

`mini_agent.py` prints two lines: a greeting, and the result of
`23 * 7 + 4 = 165`.
