# Chapter 9 — LangGraph Fundamentals: State, Nodes, Edges

This chapter teaches the LangGraph mental model: state, nodes, edges,
reducers, and Pregel-style super-steps. The lab rewrites the Chapter 5
research agent as an explicit `StateGraph` with two branches — a math
branch and a research branch that fans out in parallel.

## Files

| File | What it shows |
|---|---|
| `01_counter_graph.py` | The smallest useful graph: one node, a conditional edge, and a loop that counts to three. |
| `02_conditional_edges.py` | `add_conditional_edges` with a `path_map` that routes a support question to billing, tech, or a human. |
| `03_command_object.py` | The `Command` object: a node that updates state and picks the next node in one step. |
| `04_send_fanout.py` | `Send` fan-out: summarise three documents in parallel, then combine the results. |
| `05_reducers.py` | Three reducer styles: `operator.add` for lists, `add_messages` for chat history, and a hand-written "keep last five" reducer. |
| `06_visualize_graph.py` | Draws the compiled counter graph as Mermaid source (and PNG, if the extra dependency is available). |
| `07_support_routing_graph.py` | The chapter's worked example: a full customer-support routing graph. |
| `08_solved_problems.py` | Solutions to Problem 9.1 (even/odd loop) and Problem 9.2 (order-preserving union reducer). |
| `09_lab_research_agent_graph.py` | **Lab 9.1.** The Chapter 5 research agent rewritten as a `StateGraph`, with a math branch and a research branch that fans out to web-search and Wikipedia nodes in parallel. |

## How to run

No API keys are needed for this chapter — every example uses stub
functions instead of real LLM or search calls, exactly as printed in
the book.

Install the one package these files need:

```bash
pip install langgraph
```

Then run any file directly, for example:

```bash
python 01_counter_graph.py
python 09_lab_research_agent_graph.py
```

To try the mini-project or programming exercises, copy the closest
matching file as a starting point and change the state schema, nodes,
or routing rules as instructed in the book.
