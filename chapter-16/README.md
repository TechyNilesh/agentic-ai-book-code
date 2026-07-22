# Chapter 16 — Inside Real Agent Harnesses

This chapter dissects three real agent harnesses (Hermes Agent, OpenClaw,
and Claude Code) and ends with Lab 16.1: building a minimal harness of
your own.

## Files

- `minimal_harness.py` — the ~35-line minimal harness from Lab 16.1:
  a system-prompt builder (the "soul"), a tool table, a permission gate,
  and the agentic loop. It imports `my_llm.call_model`, a stub for any
  chat-model client — wire it to `langchain_openai`, `langchain_anthropic`,
  or a local Ollama model as an exercise (Programming Exercise 1 in the
  chapter).

## How to run

The file is a skeleton on purpose. Implement `my_llm.py` with a
`call_model(messages)` function that returns an object with `.text` and
`.tool_calls`, then:

```bash
python minimal_harness.py
```

The chapter's programming exercises walk you through adding a real model,
more tools, and a soul file.
