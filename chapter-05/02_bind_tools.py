"""
Chapter 5 - Tool Use and Function Calling
Binding tools to a chat model and reading back reply.tool_calls.

A tool definition does nothing on its own. Binding attaches the tool
schemas to every request the model receives.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the product."""
    return a * b


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return the top results as a string."""
    return f"Top {max_results} results for: {query}"


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([multiply, web_search])

    reply = llm_with_tools.invoke("What is 23 times 47?")
    print(reply.tool_calls)
    # Example shape of an entry in reply.tool_calls:
    # [{'name': 'multiply',
    #   'args': {'a': 23, 'b': 47},
    #   'id': 'call_abc123',
    #   'type': 'tool_call'}]


if __name__ == "__main__":
    main()
