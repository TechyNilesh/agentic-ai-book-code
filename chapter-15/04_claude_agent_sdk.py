"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

Claude Agent SDK: the lightest of the frameworks compared in this
chapter. You send a prompt and a tool list, and Claude runs the
native tool-use loop (Section 15.5, "Anthropic Claude Agent SDK").

Set your API key:

    export ANTHROPIC_API_KEY=sk-ant-...

Run:
    python 04_claude_agent_sdk.py
"""

import asyncio

from claude_agent_sdk import query


async def main():
    async for message in query(
        prompt="Summarise the README in this folder.",
        options={"allowed_tools": ["Read", "Grep"]},
    ):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
