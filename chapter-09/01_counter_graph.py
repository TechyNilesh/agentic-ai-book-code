"""
Chapter 9 - Building Your First StateGraph

A counter graph. It has one node that adds one to a counter, and it
loops until the counter reaches three.

Run:
    python 01_counter_graph.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class CounterState(TypedDict):
    count: int


def increment(state: CounterState) -> dict:
    new_count = state["count"] + 1
    print(f"increment: {state['count']} -> {new_count}")
    return {"count": new_count}


def should_continue(state: CounterState) -> str:
    if state["count"] < 3:
        return "increment"
    return END


builder = StateGraph(CounterState)
builder.add_node("increment", increment)
builder.add_edge(START, "increment")
builder.add_conditional_edges("increment", should_continue)
graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke({"count": 0})
    print("final:", result)
