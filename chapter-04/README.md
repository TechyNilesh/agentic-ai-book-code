# Chapter 4 -- Reasoning and Planning

This lab shows four small ways to make an LLM reason better before it
answers: Chain-of-Thought, self-consistency voting, and two versions of
ReAct (a loop that alternates Thought, Action, and Observation). The
first ReAct version is built by hand with raw API calls and a text
parser. The second uses LangGraph's `create_react_agent` prebuilt, which
does the same job in a few lines using native tool-calling.

## Files

- `01_zero_shot_cot.py` -- asks the model to "think step by step" on a word problem (Listing 4.1).
- `02_self_consistency.py` -- runs the same prompt 5 times and votes on the answer (Listing 4.2).
- `03_react_scratch.py` -- a hand-written ReAct loop with a `calculator` tool and a text parser (Listings 4.3-4.4).
- `04_react_prebuilt.py` -- the same ReAct agent built with LangGraph's `create_react_agent` (Listing 4.5).

## How to run

Install the packages:

```bash
pip install langchain-openai langgraph
```

Set your API key:

```bash
export OPENAI_API_KEY=sk-...
```

Then run any file:

```bash
python 01_zero_shot_cot.py
python 02_self_consistency.py
python 03_react_scratch.py
python 04_react_prebuilt.py
```

No file needs any other setup. Each script prints its result to the
terminal.
