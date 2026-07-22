"""Chapter 13 - A LangGraph agent that uses an MCP server.

Launches 01_echo_server.py as a subprocess over stdio, wraps its
"echo" tool as a LangChain tool via langchain-mcp-adapters, and lets a
ReAct agent call it.

Env vars needed:
    ANTHROPIC_API_KEY - your Anthropic API key

Run (from this directory, so the relative server path resolves):
    python 02_echo_agent.py
"""
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic


async def main():
    client = MultiServerMCPClient({
        "echo": {
            "command": "python",
            "args": ["01_echo_server.py"],
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()

    model = ChatAnthropic(model="claude-sonnet-4-5")
    agent = create_react_agent(model, tools)

    result = await agent.ainvoke(
        {"messages": [{"role": "user",
                       "content": "Echo the word 'hello' for me."}]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running this script.")
    asyncio.run(main())
