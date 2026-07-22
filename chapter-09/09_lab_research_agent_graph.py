"""
Chapter 9 - Lab 9.1: Rewrite the Research Agent as a LangGraph

Rewrites the Chapter 5 ReAct-style research agent as an explicit
StateGraph with two branches: one for math questions, one for research
questions. The research branch fans out to a web-search node and a
Wikipedia node in parallel using Send, then both feed into a shared
synthesise node.

The tool functions (calc_tool, web_search, wiki_lookup, llm) are stubs,
exactly as in the book. Replace them with the real tools from Chapter 5
for a working agent.

Run:
    python 09_lab_research_agent_graph.py
"""

from typing import TypedDict, Annotated, Literal
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send, Command


# Replace these stubs with the real tools from Ch 5.
def calc_tool(expr: str) -> str:
    return str(eval(expr, {"__builtins__": {}}))


def web_search(q: str) -> str:
    return f"[web] top result for: {q}"


def wiki_lookup(q: str) -> str:
    return f"[wiki] article summary for: {q}"


def llm(prompt: str) -> str:
    return f"Answer based on: {prompt[:200]}"


class AgentState(TypedDict):
    question: str
    branch: str
    facts: Annotated[list[str], add]
    answer: str


def classify(state: AgentState) -> Command[Literal["math", "research"]]:
    q = state["question"].lower()
    is_math = any(op in q for op in ["+", "-", "*", "/", "sum", "product"])
    target = "math" if is_math else "research"
    return Command(update={"branch": target}, goto=target)


def math(state: AgentState) -> dict:
    expr = state["question"].split("=")[-1].strip().strip("?")
    result = calc_tool(expr)
    return {"facts": [f"calc({expr}) = {result}"]}


def research(state: AgentState) -> list[Send]:
    return [
        Send("web", {"q": state["question"]}),
        Send("wiki", {"q": state["question"]}),
    ]


def web(payload: dict) -> dict:
    return {"facts": [web_search(payload["q"])]}


def wiki(payload: dict) -> dict:
    return {"facts": [wiki_lookup(payload["q"])]}


def synthesise(state: AgentState) -> dict:
    prompt = (
        f"Question: {state['question']}\n"
        f"Facts: {state['facts']}\n"
        "Write a short answer."
    )
    return {"answer": llm(prompt)}


builder = StateGraph(AgentState)
builder.add_node("classify", classify)
builder.add_node("math", math)
builder.add_node("research", research)
builder.add_node("web", web)
builder.add_node("wiki", wiki)
builder.add_node("synthesise", synthesise)

builder.add_edge(START, "classify")
builder.add_edge("math", "synthesise")
builder.add_conditional_edges("research", lambda s: s, ["web", "wiki"])
builder.add_edge("web", "synthesise")
builder.add_edge("wiki", "synthesise")
builder.add_edge("synthesise", END)

graph = builder.compile()


if __name__ == "__main__":
    # Run 1 -- a math question.
    print(graph.invoke({"question": "What is 23 * 17?", "facts": []}))
    # branch = 'math'
    # facts = ['calc(23 * 17) = 391']
    # answer = 'Answer based on: Question: ...'

    # Run 2 -- a research question.
    print(graph.invoke({
        "question": "Who founded the city of Hyderabad?",
        "facts": []
    }))
    # branch = 'research'
    # facts = ['[web] top result for: ...', '[wiki] article summary for: ...']
    # answer = 'Answer based on: Question: ...'
