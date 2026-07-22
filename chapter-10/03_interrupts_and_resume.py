"""
Chapter 10 - Interrupting for Human Approval, and Resuming

Shows both interrupt styles from the book:
  1. Static interrupt: interrupt_before=[...] at compile time.
  2. Dynamic interrupt: interrupt(value) called inside a node.

And how to resume a paused graph with Command(resume=value).

This assembles the book's fragments into one small runnable graph: an
approval_node that pauses, and a driver that resumes it.

Run:
    python 03_interrupts_and_resume.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command


class TxnState(TypedDict):
    amount: int
    approved: bool


# --- Dynamic interrupt inside a node ---
def approval_node(state: TxnState) -> dict:
    decision = interrupt({
        "question": "Approve this transfer?",
        "amount": state["amount"],
    })
    return {"approved": decision == "yes"}


builder = StateGraph(TxnState)
builder.add_node("approval_node", approval_node)
builder.add_edge(START, "approval_node")
builder.add_edge("approval_node", END)

# Static interrupt style, shown for reference (not used below):
#
#   graph = builder.compile(
#       checkpointer=saver,
#       interrupt_before=["execute_payment"],
#   )


if __name__ == "__main__":
    with SqliteSaver.from_conn_string("interrupts_demo.db") as saver:
        graph = builder.compile(checkpointer=saver)
        cfg = {"configurable": {"thread_id": "txn-42"}}

        out = graph.invoke({"amount": 4500, "approved": False}, config=cfg)
        print("Pending decision:", out.get("__interrupt__"))

        # The human said "yes". Resume the paused graph:
        result = graph.invoke(Command(resume="yes"), config=cfg)
        print("Result:", result)
