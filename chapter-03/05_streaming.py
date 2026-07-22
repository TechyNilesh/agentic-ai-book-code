"""
Chapter 3: Streaming and async.

Use .stream() for a responsive UI in synchronous code. Use
.astream() inside an asyncio program when you also need to do other
I/O concurrently.

Setup:
    pip install -r requirements.txt

Run:
    python 05_streaming.py
"""

import asyncio

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient tutor for Indian engineering students."),
    ("human", "Explain {topic} in {language} using a simple analogy."),
])

chain = prompt | claude | StrOutputParser()


def sync_stream_demo() -> None:
    for chunk in chain.stream({"topic": "LSTM", "language": "English"}):
        print(chunk, end="", flush=True)
    print()


async def async_stream_demo() -> None:
    async for chunk in chain.astream(
        {"topic": "self-attention", "language": "English"}
    ):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    sync_stream_demo()
    asyncio.run(async_stream_demo())
