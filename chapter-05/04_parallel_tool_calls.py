"""
Chapter 5 - Tool Use and Function Calling
Dispatching several tool calls in parallel with a thread pool.

Modern models can request several tool calls in one turn (for example,
"weather in Mumbai and time in Tokyo"). Running them through a
ThreadPoolExecutor cuts wall-clock time for I/O-bound tools.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
from concurrent.futures import ThreadPoolExecutor

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """Return a made-up current weather report for a city."""
    return f"It is sunny in {city}."


@tool
def get_time(city: str) -> str:
    """Return a made-up current local time for a city."""
    return f"It is 10:00 AM in {city}."


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([get_weather, get_time])

    tools_by_name = {"get_weather": get_weather, "get_time": get_time}
    messages = [HumanMessage("What is the weather in Mumbai and the time in Tokyo?")]

    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)

    def run_call(call):
        fn = tools_by_name[call["name"]]
        try:
            out = fn.invoke(call["args"])
        except Exception as e:
            out = f"ERROR: {e}"
        return ToolMessage(content=str(out), tool_call_id=call["id"])

    with ThreadPoolExecutor(max_workers=4) as ex:
        tool_msgs = list(ex.map(run_call, ai_msg.tool_calls))

    messages.extend(tool_msgs)

    final = llm_with_tools.invoke(messages)
    print(final.content)


if __name__ == "__main__":
    main()
