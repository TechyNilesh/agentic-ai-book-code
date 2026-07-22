"""
Chapter 5 - Tool Use and Function Calling
Running tool calls, handling errors, and retrying flaky tools.

After the model emits a tool call, run the tool and append a
ToolMessage with the result, wrapped in try/except so a bad call
becomes an observation instead of a crash. call_with_retry() shows
exponential backoff for flaky network tools.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
import time

from langchain_core.messages import HumanMessage, ToolMessage
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


def call_with_retry(fn, args, attempts: int = 3, delay: float = 1.0):
    """Exponential backoff for flaky network tools."""
    for i in range(attempts):
        try:
            return fn.invoke(args)
        except Exception as e:
            if i == attempts - 1:
                return f"ERROR after {attempts} tries: {e}"
            time.sleep(delay * (2 ** i))


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([multiply, web_search])

    tools_by_name = {"multiply": multiply, "web_search": web_search}
    messages = [HumanMessage("What is 23 times 47?")]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    for call in ai_msg.tool_calls:
        try:
            result = tools_by_name[call["name"]].invoke(call["args"])
        except Exception as e:
            result = f"ERROR: {type(e).__name__}: {e}"
        messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    final = llm_with_tools.invoke(messages)
    print(final.content)


if __name__ == "__main__":
    main()
