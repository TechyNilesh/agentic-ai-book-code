"""
Chapter 9 - Reducers: Merging Updates

Shows the three reducer styles from the book:
  1. operator.add for lists
  2. add_messages for chat history
  3. a hand-written reducer that keeps only the last five entries

These are schema fragments from the book, collected here for reference.
Run this file to see them used inside a tiny graph.

Run:
    python 05_reducers.py
"""

from operator import add
from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage


# --- Book fragment: operator.add for a log list ---
class LogState(TypedDict):
    log: Annotated[list[str], add]


# --- Book fragment: add_messages for chat history ---
class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


# --- Book fragment: a custom reducer that keeps only the last five items ---
def keep_last_five(old: list, new: list) -> list:
    return (old + new)[-5:]


class RecentState(TypedDict):
    recent: Annotated[list, keep_last_five]


def append_log(state: LogState) -> dict:
    return {"log": ["step ran"]}


def build_log_graph():
    builder = StateGraph(LogState)
    builder.add_node("append_log", append_log)
    builder.add_edge(START, "append_log")
    builder.add_edge("append_log", END)
    return builder.compile()


if __name__ == "__main__":
    graph = build_log_graph()
    out = graph.invoke({"log": ["start"]})
    print("log reducer demo:", out)

    # add_messages demo: two updates with the same id merge into one message.
    merged = add_messages(
        [HumanMessage(content="hi", id="m1")],
        [AIMessage(content="hello!", id="m2")],
    )
    print("add_messages demo:", merged)

    # keep_last_five demo
    print("keep_last_five demo:", keep_last_five([1, 2, 3, 4, 5], [6, 7]))
