"""
Chapter 8 - Multi-Agent Systems
Lab: Research-writing crew in LangGraph.

A five-agent crew (Planner, Researcher, Writer, Editor, Reviewer) takes
a topic and produces a short brief. A supervisor node routes among the
workers based on the shared state, until the Reviewer approves the
draft or MAX_TURNS is reached.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
from typing import Literal, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class CrewState(TypedDict):
    topic: str
    outline: str
    notes: str
    draft: str
    edited: bool
    feedback: str
    approved: bool
    turns: int


MAX_TURNS = 12


def planner(state: CrewState):
    prompt = f"Create a 5-point outline for a 300-word brief on: {state['topic']}"
    out = llm.invoke(prompt).content
    return {"outline": out, "turns": state["turns"] + 1}


def researcher(state: CrewState):
    prompt = (
        f"Topic: {state['topic']}\nOutline: {state['outline']}\n"
        "List 4 factual bullet notes a writer will need."
    )
    out = llm.invoke(prompt).content
    return {"notes": out, "turns": state["turns"] + 1}


def writer(state: CrewState):
    prompt = (
        f"Write a 300-word brief on '{state['topic']}'.\n"
        f"Outline:\n{state['outline']}\nNotes:\n{state['notes']}\n"
        f"Feedback (if any): {state.get('feedback', '')}"
    )
    out = llm.invoke(prompt).content
    return {"draft": out, "edited": False, "approved": False, "turns": state["turns"] + 1}


def editor(state: CrewState):
    prompt = (
        "Edit this brief for clarity and length (~300 words). "
        f"Return only the edited text.\n\n{state['draft']}"
    )
    out = llm.invoke(prompt).content
    return {"draft": out, "edited": True, "turns": state["turns"] + 1}


def reviewer(state: CrewState):
    prompt = (
        "Review this brief against the notes. "
        "If accurate and clear, reply 'APPROVE'. "
        "Otherwise reply with one short paragraph of feedback.\n\n"
        f"Notes:\n{state['notes']}\n\nDraft:\n{state['draft']}"
    )
    out = llm.invoke(prompt).content.strip()
    if out.upper().startswith("APPROVE"):
        return {"approved": True, "turns": state["turns"] + 1}
    return {
        "approved": False,
        "feedback": out,
        "edited": False,
        "turns": state["turns"] + 1,
    }


def supervisor(
    state: CrewState,
) -> Command[Literal["planner", "researcher", "writer", "editor", "reviewer", "__end__"]]:
    if state["turns"] >= MAX_TURNS or state.get("approved"):
        return Command(goto=END)
    if not state.get("outline"):
        return Command(goto="planner")
    if not state.get("notes"):
        return Command(goto="researcher")
    if not state.get("draft"):
        return Command(goto="writer")
    if state.get("feedback") and not state.get("edited"):
        return Command(goto="writer")
    if not state.get("edited"):
        return Command(goto="editor")
    return Command(goto="reviewer")


def build_graph():
    g = StateGraph(CrewState)
    g.add_node("supervisor", supervisor)
    g.add_node("planner", planner)
    g.add_node("researcher", researcher)
    g.add_node("writer", writer)
    g.add_node("editor", editor)
    g.add_node("reviewer", reviewer)

    g.add_edge(START, "supervisor")
    for n in ["planner", "researcher", "writer", "editor", "reviewer"]:
        g.add_edge(n, "supervisor")

    return g.compile()


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    app = build_graph()
    result = app.invoke(
        {
            "topic": "agentic RAG",
            "outline": "",
            "notes": "",
            "draft": "",
            "edited": False,
            "feedback": "",
            "approved": False,
            "turns": 0,
        }
    )
    print(result["draft"])


if __name__ == "__main__":
    main()
