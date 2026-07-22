"""Chapter 13 - Lab 13.1: A SQLite MCP server.

Exposes a SQLite database as three tools: list_tables, describe, and
query (SELECT-only). Run 06_seed_db.py first to create shop.db, then
run this as a subprocess from 07_sqlite_agent.py.

No API key needed -- this file only needs the `mcp` package (and the
standard library sqlite3 module).
"""
import asyncio, sqlite3, json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

DB = "shop.db"
server = Server("sqlite-server")


@server.list_tools()
async def list_tools():
    return [
        Tool(name="list_tables",
             description="List all tables in the database.",
             inputSchema={"type": "object", "properties": {}}),
        Tool(name="describe",
             description="Return the schema of a table.",
             inputSchema={"type": "object",
                          "properties": {"table": {"type": "string"}},
                          "required": ["table"]}),
        Tool(name="query",
             description="Run a SELECT query. Reject non-SELECT.",
             inputSchema={"type": "object",
                          "properties": {"sql": {"type": "string"}},
                          "required": ["sql"]}),
    ]


@server.call_tool()
async def call_tool(name, args):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    if name == "list_tables":
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        out = [r[0] for r in cur.fetchall()]
    elif name == "describe":
        cur.execute(f"PRAGMA table_info({args['table']})")
        out = cur.fetchall()
    elif name == "query":
        sql = args["sql"].strip()
        if not sql.lower().startswith("select"):
            return [TextContent(type="text", text="Only SELECT allowed.")]
        cur.execute(sql)
        out = cur.fetchall()
    else:
        out = f"Unknown tool {name}"
    return [TextContent(type="text", text=json.dumps(out, default=str))]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
