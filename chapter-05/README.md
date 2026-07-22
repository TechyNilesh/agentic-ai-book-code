# Chapter 5 -- Tool Use and Function Calling

This lab shows how to give an LLM the power to call real functions:
defining tools, binding them to a model, handling their output and
errors, running several tool calls in parallel, and finally building a
five-tool research agent that puts it all together.

## Files

- `01_tool_basics.py` -- defines a tool with `@tool` and a stricter one with a Pydantic `args_schema`; prints the generated JSON schemas.
- `02_bind_tools.py` -- binds tools to a chat model with `bind_tools` and reads `reply.tool_calls`.
- `03_tool_loop_with_errors_and_retry.py` -- the full loop: call the model, run the tool in a try/except, send a `ToolMessage` back, and an exponential-backoff retry helper for flaky tools.
- `04_parallel_tool_calls.py` -- dispatches multiple tool calls from one model turn using a `ThreadPoolExecutor`.
- `05_date_calculator_agent.py` -- worked example with two tools (`days_until`, `add`); shows the model picking the right tool, or no tool at all.
- `06_five_tool_research_agent.py` -- the chapter lab: a `create_react_agent` with web search, calculator, Wikipedia, a calendar stub, and a sandboxed Python REPL.

## How to run

Install the packages:

```bash
pip install langchain langchain-openai langchain-community langgraph \
            duckduckgo-search wikipedia numexpr
```

Set your API key:

```bash
export OPENAI_API_KEY=sk-...
```

Then run any file, for example:

```bash
python 01_tool_basics.py
python 06_five_tool_research_agent.py
```

`06_five_tool_research_agent.py` calls the live web through DuckDuckGo
and Wikipedia, so it needs an internet connection. Its `python_repl`
tool runs code in a subprocess with a 5-second timeout -- do not remove
that timeout when you extend the tool.
