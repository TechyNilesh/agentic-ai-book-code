"""
Chapter 4 - Reasoning and Planning
Listing 4.5: ReAct using LangGraph's prebuilt create_react_agent.

The same idea as 03_react_scratch.py, but LangGraph's prebuilt does the
loop for us in about ten lines, using the model's native tool-calling
API instead of text parsing.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '17 * 23 + 9'."""
    return str(eval(expression, {"__builtins__": {}}, {}))


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = create_react_agent(llm, tools=[calculator])

    result = agent.invoke({"messages": [("user", "What is 17 * 23 + 9?")]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
