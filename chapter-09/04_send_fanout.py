"""
Chapter 9 - Fan-Out with Send

Send() schedules several parallel runs of the same target node, each
with its own payload. Here we summarise three documents in parallel and
then combine the summaries.

Run:
    python 04_send_fanout.py
"""

from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class BatchState(TypedDict):
    documents: list
    summaries: Annotated[list, add]


def loader(state: BatchState) -> dict:
    # In the book this node just passes the documents through.
    return {}


# --- Book fragment ---
def fan_out(state: BatchState) -> list[Send]:
    return [
        Send("summarise_one", {"doc": d})
        for d in state["documents"]
    ]


def summarise_one(payload: dict) -> dict:
    text = payload["doc"]
    return {"summaries": [text[:80] + "..."]}


def combine(state: BatchState) -> dict:
    return {}


builder = StateGraph(BatchState)
builder.add_node("loader", loader)
builder.add_node("summarise_one", summarise_one)
builder.add_node("combine", combine)
builder.add_edge(START, "loader")
builder.add_conditional_edges("loader", fan_out, ["summarise_one"])
builder.add_edge("summarise_one", "combine")
builder.add_edge("combine", END)
graph = builder.compile()


if __name__ == "__main__":
    docs = [
        "Document one is about transformers and attention.",
        "Document two is about vector databases and retrieval.",
        "Document three is about LangGraph and state machines.",
    ]
    result = graph.invoke({"documents": docs, "summaries": []})
    for s in result["summaries"]:
        print(s)
