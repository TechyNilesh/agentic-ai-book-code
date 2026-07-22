"""
Chapter 10 - Lab: HITL Travel-Booking Agent (SqliteSaver)

Goal: build an agent that searches flights, drafts a booking, pauses
for human approval, and on "yes" books the flight. Uses SqliteSaver so
progress survives restarts.

Setup:
    pip install langgraph langgraph-checkpoint-sqlite

Run:
    python 08_lab_travel_booking_agent.py

What to verify (from the book):
  1. Delete travel.db between runs to start fresh; otherwise the same
     thread_id resumes.
  2. Try Command(resume="no") -- booking_ref should be "CANCELLED".
  3. Kill the script after the first invoke() returns. Restart and pass
     Command(resume="yes") -- it still books.
  4. Run g.get_state_history(cfg) and count the snapshots. There should
     be one per super-step.
"""

from typing import TypedDict, List

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command


class TripState(TypedDict):
    origin: str
    destination: str
    flights: List[dict]
    proposal: dict
    approved: bool
    booking_ref: str


# --- Nodes ---
def search_flights(s: TripState) -> TripState:
    # In real code, call an API. Here we stub.
    flights = [
        {"id": "AI101", "fare": 6200, "dep": "08:00"},
        {"id": "6E223", "fare": 5400, "dep": "11:30"},
        {"id": "UK987", "fare": 7100, "dep": "18:45"},
    ]
    return {"flights": flights}


def draft_proposal(s: TripState) -> TripState:
    cheapest = min(s["flights"], key=lambda f: f["fare"])
    return {"proposal": cheapest}


def human_approval(s: TripState) -> TripState:
    decision = interrupt({
        "question": f"Book {s['proposal']['id']} for "
                    f"INR {s['proposal']['fare']}?",
        "proposal": s["proposal"],
    })
    return {"approved": decision == "yes"}


def book(s: TripState) -> TripState:
    if not s["approved"]:
        return {"booking_ref": "CANCELLED"}
    # Stub: real code would call the airline API
    return {"booking_ref": f"PNR-{s['proposal']['id']}-OK"}


# --- Graph ---
b = StateGraph(TripState)
b.add_node("search", search_flights)
b.add_node("draft", draft_proposal)
b.add_node("approve", human_approval)
b.add_node("book", book)
b.add_edge(START, "search")
b.add_edge("search", "draft")
b.add_edge("draft", "approve")
b.add_edge("approve", "book")
b.add_edge("book", END)


if __name__ == "__main__":
    # --- Run ---
    with SqliteSaver.from_conn_string("travel.db") as saver:
        g = b.compile(checkpointer=saver)
        cfg = {"configurable": {"thread_id": "trip-mum-blr-1"}}

        # First call: runs until interrupt()
        out = g.invoke({
            "origin": "BOM", "destination": "BLR",
            "flights": [], "proposal": {},
            "approved": False, "booking_ref": ""
        }, config=cfg)
        print("Pending decision:", out.get("__interrupt__"))

        # ---- Imagine the process is killed here. ----
        # ---- A web UI shows the proposal to the user. ----
        # ---- User clicks "Approve". We come back: ----

        final = g.invoke(Command(resume="yes"), config=cfg)
        print("Booking:", final["booking_ref"])
