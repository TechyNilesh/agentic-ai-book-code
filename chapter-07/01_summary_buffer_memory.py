"""
Chapter 7 - Memory in Agentic Systems
Listing: Summary buffer in LangChain.

ConversationSummaryBufferMemory keeps recent turns verbatim and
summarises older ones once the token budget is crossed. This is a
simple way to manage a growing context window.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os

from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini")
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=400,  # summarise when above this
        return_messages=True,
    )

    # Illustrative use: save a couple of turns and inspect the buffer.
    memory.save_context({"input": "Hi, I'm Aarav."}, {"output": "Hello Aarav!"})
    memory.save_context(
        {"input": "I'm vegetarian."}, {"output": "Noted, I'll avoid meat."}
    )
    print(memory.load_memory_variables({}))


if __name__ == "__main__":
    main()
