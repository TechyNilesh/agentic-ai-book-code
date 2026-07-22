"""
Chapter 9 - Worked Example: A Routing Customer-Support Graph

Reads a question, classifies it, routes to a sub-agent, and ends.

Run:
    python 07_support_routing_graph.py
"""

from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END


class SupportState(TypedDict):
    question: str
    category: str
    log: Annotated[list[str], add]
    answer: str


def intake(state: SupportState) -> dict:
    return {"log": ["intake: received question"]}


def classify(state: SupportState) -> str:
    q = state["question"].lower()
    if any(w in q for w in ["refund", "bill", "invoice"]):
        return "billing"
    if any(w in q for w in ["error", "crash", "bug"]):
        return "tech"
    return "human"


def billing_agent(state: SupportState) -> dict:
    return {
        "category": "billing",
        "log": ["billing_agent ran"],
        "answer": "Please share your invoice number; refunds take 5 days.",
    }


def tech_agent(state: SupportState) -> dict:
    return {
        "category": "technical",
        "log": ["tech_agent ran"],
        "answer": "Try restarting and share the error log.",
    }


def human_agent(state: SupportState) -> dict:
    return {
        "category": "human",
        "log": ["human_agent ran"],
        "answer": "A human will call you in 30 minutes.",
    }


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
        "human": "human_agent",
    },
)
builder.add_edge("billing_agent", END)
builder.add_edge("tech_agent", END)
builder.add_edge("human_agent", END)

graph = builder.compile()


if __name__ == "__main__":
    out = graph.invoke({"question": "I want a refund for my last invoice."})
    print(out["answer"])
    print(out["log"])
