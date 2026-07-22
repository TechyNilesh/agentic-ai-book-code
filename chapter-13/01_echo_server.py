"""Chapter 13 - A tiny stdio MCP server.

The simplest possible MCP server: one tool, "echo", that returns the
input string unchanged. Run this as a subprocess from an MCP client
(see 02_echo_agent.py) -- you never start it directly for its own sake,
though `python 01_echo_server.py` will run and wait on stdio.

No API key needed -- this file only needs the `mcp` package.
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("echo-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="echo",
            description="Return the input string unchanged.",
            inputSchema={
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, args: dict) -> list[TextContent]:
    if name == "echo":
        return [TextContent(type="text", text=args["text"])]
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
