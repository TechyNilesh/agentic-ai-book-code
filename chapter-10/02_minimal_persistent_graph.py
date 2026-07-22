"""
Chapter 10 - Running with a Checkpointer

The smallest possible persistent graph: a two-node graph that counts.
Uses SqliteSaver, and the thread_id / config pattern from the book.

Run:
    python 02_minimal_persistent_graph.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


class S(TypedDict):
    count: int


def inc(s: S) -> S:
    return {"count": s["count"] + 1}


builder = StateGraph(S)
builder.add_node("inc", inc)
builder.add_edge(START, "inc")
builder.add_edge("inc", END)


if __name__ == "__main__":
    with SqliteSaver.from_conn_string("counter.db") as saver:
        graph = builder.compile(checkpointer=saver)
        cfg = {"configurable": {"thread_id": "demo"}}

        print(graph.invoke({"count": 0}, config=cfg))  # {'count': 1}
        print(graph.invoke(None, config=cfg))           # {'count': 2}
        print(graph.invoke(None, config=cfg))           # {'count': 3}
