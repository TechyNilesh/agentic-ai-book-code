"""
Chapter 5 - Tool Use and Function Calling
Lab: A Five-Tool Research Agent.

An agent with five tools: web search, calculator, Wikipedia lookup,
a calendar stub, and a sandboxed Python REPL. Built with LangGraph's
create_react_agent prebuilt.

requirements: langchain, langchain-openai, langchain-community,
duckduckgo-search, wikipedia, numexpr, langgraph

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
import subprocess
import tempfile

import numexpr
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# 1. Web search
_ddg = DuckDuckGoSearchRun()


@tool
def web_search(query: str) -> str:
    """Search the live web for recent information. Use for news,
    prices, or anything that may have changed since training."""
    return _ddg.run(query)


# 2. Calculator
@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression like '2*(3+4)/5'.
    Use for any numeric computation."""
    try:
        return str(numexpr.evaluate(expression).item())
    except Exception as e:
        return f"ERROR: {e}"


# 3. Wikipedia
_wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1200)


@tool
def wikipedia(topic: str) -> str:
    """Look up a topic on Wikipedia. Use for stable facts about
    people, places, history, and science."""
    return _wiki.run(topic)


# 4. Calendar stub
_CAL = []


@tool
def add_event(title: str, date_iso: str) -> str:
    """Add an event to the user's calendar.
    date_iso must be YYYY-MM-DD."""
    _CAL.append({"title": title, "date": date_iso})
    return f"Saved: {title} on {date_iso}"


# 5. Sandboxed Python REPL
@tool
def python_repl(code: str) -> str:
    """Run a short Python snippet in a sandbox and return stdout.
    Use for data manipulation that the calculator cannot handle."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        out = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=5,
            env={"PATH": os.environ.get("PATH", "")},
        )
        return (out.stdout or out.stderr)[:1500]
    except subprocess.TimeoutExpired:
        return "ERROR: timeout"
    finally:
        os.unlink(path)


tools = [web_search, calculator, wikipedia, add_event, python_repl]


def ask(agent, q: str) -> None:
    out = agent.invoke({"messages": [("user", q)]})
    print("Q:", q)
    print("A:", out["messages"][-1].content, "\n")


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools)

    ask(
        agent,
        "Who wrote the novel Midnight's Children and in what year? "
        "Also compute 1981 * 7.",
    )
    ask(
        agent,
        "Schedule a meeting called 'Project Review' on 2026-06-01, "
        "then tell me what's on my calendar.",
    )


if __name__ == "__main__":
    main()
