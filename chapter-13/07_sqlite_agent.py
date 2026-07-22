"""Chapter 13 - Lab 13.1: client for the SQLite MCP server.

The book says: "Reuse the LangGraph agent code from the worked example,
swapping in sqlite_server.py." This file is that reuse -- same pattern
as 04_weather_agent.py, pointed at 05_sqlite_server.py, asking a
question about the shop database.

Env vars needed:
    ANTHROPIC_API_KEY - your Anthropic API key

Run (from this directory, after `python 06_seed_db.py`):
    python 07_sqlite_agent.py
"""
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic


async def main():
    client = MultiServerMCPClient({
        "shop": {"command": "python",
                 "args": ["05_sqlite_server.py"],
                 "transport": "stdio"}
    })
    tools = await client.get_tools()
    agent = create_react_agent(ChatAnthropic(model="claude-sonnet-4-5"),
                                tools)
    out = await agent.ainvoke({"messages":
        [{"role": "user",
          "content": "Which 5 customers spent the most last month?"}]})
    print(out["messages"][-1].content)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running this script.")
    asyncio.run(main())
