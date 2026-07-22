"""
Chapter 10 - Worked Example: A Long-Running Research Agent that
Survives Restart

Three nodes: search, summarise, write_report. Each has an artificial
5-second delay so you can kill the process between steps and see it
resume from the last checkpoint.

Run:
    python 06_durable_research_agent.py

Try it: while "summarise" is sleeping, press Ctrl-C, then run the
script again. "search" will not re-run -- it already finished and its
result was checkpointed.
"""

import time
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


class S(TypedDict):
    topic: str
    sources: list
    summary: str
    report: str


def search(s: S) -> S:
    print("[search] working...")
    time.sleep(5)
    return {"sources": [f"src-{i} on {s['topic']}" for i in range(3)]}


def summarise(s: S) -> S:
    print("[summarise] working...")
    time.sleep(5)
    return {"summary": f"Summary of {len(s['sources'])} sources."}


def write_report(s: S) -> S:
    print("[write_report] working...")
    time.sleep(5)
    return {"report": f"# Report\n{s['summary']}"}


b = StateGraph(S)
b.add_node("search", search)
b.add_node("summarise", summarise)
b.add_node("write_report", write_report)
b.add_edge(START, "search")
b.add_edge("search", "summarise")
b.add_edge("summarise", "write_report")
b.add_edge("write_report", END)


if __name__ == "__main__":
    with SqliteSaver.from_conn_string("research.db") as saver:
        g = b.compile(checkpointer=saver)
        cfg = {"configurable": {"thread_id": "topic-quantum"}}
        out = g.invoke({"topic": "quantum computing",
                        "sources": [], "summary": "", "report": ""},
                       config=cfg)
        print(out["report"])
