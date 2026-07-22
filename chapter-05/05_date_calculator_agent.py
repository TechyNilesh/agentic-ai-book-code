"""
Chapter 5 - Tool Use and Function Calling
Worked example: a two-tool date-calculator agent.

Two tools are registered: days_until (date math) and add (arithmetic).
We bind both to the model and let it pick the right one -- or neither,
for a question it can answer from its own knowledge.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
from datetime import date

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def days_until(target: str) -> str:
    """Return the number of days from today until target (YYYY-MM-DD)."""
    delta = date.fromisoformat(target) - date.today()
    return f"{delta.days} days"


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def ask(llm_with_tools, tools_by_name, question: str) -> str:
    messages = [HumanMessage(question)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    for call in ai_msg.tool_calls:
        try:
            result = tools_by_name[call["name"]].invoke(call["args"])
        except Exception as e:
            result = f"ERROR: {type(e).__name__}: {e}"
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    final = llm_with_tools.invoke(messages)
    return final.content


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([days_until, add])
    tools_by_name = {"days_until": days_until, "add": add}

    # Expected: calls days_until(target="2026-12-25")
    print(ask(llm_with_tools, tools_by_name, "How many days until 2026-12-25?"))
    # Expected: calls add(a=3.14, b=2.71)
    print(ask(llm_with_tools, tools_by_name, "What is 3.14 plus 2.71?"))
    # Expected: answers directly, calls no tool
    print(ask(llm_with_tools, tools_by_name, "What is the capital of France?"))


if __name__ == "__main__":
    main()
