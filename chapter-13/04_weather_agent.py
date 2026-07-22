"""Chapter 13 - Worked Example: the weather MCP client.

Connects a LangGraph ReAct agent to 03_weather_server.py and asks a
natural-language question. The agent calls get_weather(city="Bengaluru"),
reads "light rain", and recommends carrying an umbrella.

Env vars needed:
    ANTHROPIC_API_KEY - your Anthropic API key

Run (from this directory, so the relative server path resolves):
    python 04_weather_agent.py
"""
import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic


async def main():
    client = MultiServerMCPClient({
        "weather": {"command": "python",
                    "args": ["03_weather_server.py"],
                    "transport": "stdio"}
    })
    tools = await client.get_tools()
    agent = create_react_agent(ChatAnthropic(model="claude-sonnet-4-5"),
                                tools)
    out = await agent.ainvoke({"messages":
        [{"role": "user", "content": "Should I carry an umbrella in Bengaluru today?"}]})
    print(out["messages"][-1].content)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running this script.")
    asyncio.run(main())
