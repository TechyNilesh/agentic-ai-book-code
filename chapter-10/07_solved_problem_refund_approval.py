"""
Chapter 10 - Solved Problem 10.2

A refund-issuing agent. Refunds above INR 10,000 need manager approval.
Below that, the agent acts automatically.

Run:
    python 07_solved_problem_refund_approval.py
"""

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command


class RefundState(TypedDict):
    amount: int
    approved: bool
    status: str


def needs_approval(s: RefundState) -> str:
    return "approval" if s["amount"] >= 10000 else "issue"


def approval(s: RefundState) -> dict:
    decision = interrupt({"q": "Approve?", "amt": s["amount"]})
    return {"approved": decision == "yes"}


def issue(s: RefundState) -> dict:
    # call payments API
    return {"status": "refunded"}


b = StateGraph(RefundState)
b.add_node("approval", approval)
b.add_node("issue", issue)
b.add_conditional_edges(START, needs_approval,
                         {"approval": "approval", "issue": "issue"})
b.add_edge("approval", "issue")
b.add_edge("issue", END)


if __name__ == "__main__":
    with SqliteSaver.from_conn_string("refunds.db") as saver:
        graph = b.compile(checkpointer=saver)

        # Below threshold: no approval needed.
        cfg1 = {"configurable": {"thread_id": "refund-1"}}
        print(graph.invoke({"amount": 3000, "approved": False, "status": ""},
                            config=cfg1))

        # Above threshold: pauses for manager approval.
        cfg2 = {"configurable": {"thread_id": "refund-2"}}
        out = graph.invoke({"amount": 15000, "approved": False, "status": ""},
                            config=cfg2)
        print("Pending:", out.get("__interrupt__"))

        # The manager UI calls invoke(Command(resume="yes"), config=...)
        final = graph.invoke(Command(resume="yes"), config=cfg2)
        print(final)
