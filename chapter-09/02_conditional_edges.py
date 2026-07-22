"""
Chapter 9 - Conditional Edges

Shows the add_conditional_edges() signature and a router function with a
path_map, as in the book. This file wraps the book's fragment in a small
runnable graph so you can see the routing in action.

Run:
    python 02_conditional_edges.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class SupportState(TypedDict):
    question: str
    answer: str


def intake(state: SupportState) -> dict:
    return {}


# --- Book fragment: the router function and add_conditional_edges call ---
def classify(state: SupportState) -> str:
    text = state["question"].lower()
    if "bill" in text or "refund" in text:
        return "billing"
    if "error" in text or "crash" in text:
        return "tech"
    return "fallback"


def billing_agent(state: SupportState) -> dict:
    return {"answer": "billing_agent handled this"}


def tech_agent(state: SupportState) -> dict:
    return {"answer": "tech_agent handled this"}


def human_agent(state: SupportState) -> dict:
    return {"answer": "human_agent handled this"}


builder = StateGraph(SupportState)
builder.add_node("intake", intake)
builder.add_node("billing_agent", billing_agent)
builder.add_node("tech_agent", tech_agent)
builder.add_node("human_agent", human_agent)
builder.add_edge(START, "intake")
builder.add_conditional_edges(
    "intake",
    classify,
    path_map={
        "billing": "billing_agent",
        "tech": "tech_agent",
        "fallback": "human_agent",
    },
)
builder.add_edge("billing_agent", END)
builder.add_edge("tech_agent", END)
builder.add_edge("human_agent", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"question": "I need a refund on my bill."}))
