# Chapter 8 -- Multi-Agent Systems

This lab builds a five-agent crew in LangGraph: Planner, Researcher,
Writer, Editor, and Reviewer. A supervisor node reads the shared state
and routes to the next worker, until the Reviewer approves the draft
or a turn limit is hit. It shows the supervisor pattern and a handoff
of context (not just control) through the shared `CrewState`.

## Files

- `01_research_writing_crew.py` -- the chapter lab. Builds the crew graph, runs it on the topic "agentic RAG", and prints the final approved brief.

## How to run

Install the packages:

```bash
pip install langgraph langchain-openai
```

Set your API key:

```bash
export OPENAI_API_KEY=sk-...
```

Then run:

```bash
python 01_research_writing_crew.py
```

Things to try, as suggested in the book:

1. Print the state after each node to see the flow.
2. Force the Reviewer to reject once, and watch the Writer revise using `feedback`.
3. Lower `MAX_TURNS` to 3 and see how the supervisor stops early.
