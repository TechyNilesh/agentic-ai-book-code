"""Chapter 13 - Worked Example: a weather MCP server.

Exposes one tool, "get_weather", backed by a fake in-memory database of
three Indian cities. Run this as a subprocess from 04_weather_agent.py.

No API key needed -- this file only needs the `mcp` package.
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("weather")

FAKE_DB = {
    "Bengaluru": "28 C, light rain",
    "Mumbai":    "31 C, humid",
    "Delhi":     "39 C, hazy",
}


@server.list_tools()
async def list_tools():
    return [Tool(
        name="get_weather",
        description="Return current weather for an Indian city.",
        inputSchema={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    )]


@server.call_tool()
async def call_tool(name, args):
    city = args["city"]
    text = FAKE_DB.get(city, f"No data for {city}")
    return [TextContent(type="text", text=text)]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
