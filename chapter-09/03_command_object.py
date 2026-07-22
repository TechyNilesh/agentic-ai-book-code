"""
Chapter 9 - The Command Object

A node can update state AND pick the next node in one return value, using
langgraph.types.Command. This wraps the book's intake() fragment in a
small runnable graph.

Run:
    python 03_command_object.py
"""

from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


class SupportState(TypedDict):
    question: str
    category: str
    answer: str


# --- Book fragment ---
def intake(state: SupportState) -> Command[Literal["billing", "tech"]]:
    text = state["question"].lower()
    if "bill" in text:
        return Command(
            update={"category": "billing"},
            goto="billing_agent",
        )
    return Command(
        update={"category": "technical"},
        goto="tech_agent",
    )


def billing_agent(state: SupportState) -> dict:
    return {"answer": "billing_agent handled this"}


def tech_agent(state: SupportState) -> dict:
    return {"answer": "tech_agent handled this"}


builder = StateGraph(SupportState)
builder.add_node("intake", intake)
builder.add_node("billing_agent", billing_agent)
builder.add_node("tech_agent", tech_agent)
builder.add_edge(START, "intake")
builder.add_edge("billing_agent", END)
builder.add_edge("tech_agent", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"question": "I have a billing question."}))
