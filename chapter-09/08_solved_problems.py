"""
Chapter 9 - Solved Problems 9.1 and 9.2

Problem 9.1: A graph with two nodes A and B. After A, go to B if a
counter in state is even, else loop back to A. End when the counter
reaches 4.

Problem 9.2: A reducer that keeps the union of two lists without
duplicates, preserving order of first appearance.

Run:
    python 08_solved_problems.py
"""

from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, START, END


# --- Problem 9.1 ---
class S(TypedDict):
    n: int


def a(s: S) -> dict:
    return {"n": s["n"] + 1}


def b(s: S) -> dict:
    return {"n": s["n"] + 1}


def route(s: S) -> str:
    if s["n"] >= 4:
        return END
    return "B" if s["n"] % 2 == 0 else "A"


g = StateGraph(S)
g.add_node("A", a)
g.add_node("B", b)
g.add_edge(START, "A")
g.add_conditional_edges("A", route, {"A": "A", "B": "B", END: END})
g.add_edge("B", "A")
problem_9_1_graph = g.compile()


# --- Problem 9.2 ---
def merge_tags(old: list[str], new: list[str]) -> list[str]:
    seen = set(old)
    result = list(old)
    for t in new:
        if t not in seen:
            result.append(t)
            seen.add(t)
    return result


class TagState(TypedDict):
    tags: Annotated[list[str], merge_tags]


if __name__ == "__main__":
    print("Problem 9.1:", problem_9_1_graph.invoke({"n": 0}))
    print("Problem 9.2:", merge_tags(["python", "ai"], ["ai", "langgraph"]))
