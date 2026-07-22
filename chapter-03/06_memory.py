"""
Chapter 3: Memory primitives.

A single .invoke call has no memory. We carry history ourselves
using RunnableWithMessageHistory, the LangChain 1.0 replacement for
the deprecated ConversationBufferMemory.

Setup:
    pip install -r requirements.txt

Run:
    python 06_memory.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful study buddy."),
    MessagesPlaceholder("history"),
    ("human", "{input}"),
])

chat_chain = chat_prompt | claude | StrOutputParser()

store = {}


def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


with_memory = RunnableWithMessageHistory(
    chat_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)


def main() -> None:
    cfg = {"configurable": {"session_id": "nilesh-001"}}
    print(with_memory.invoke({"input": "Hi, I am Nilesh."}, config=cfg))
    print(with_memory.invoke({"input": "What is my name?"}, config=cfg))


if __name__ == "__main__":
    main()
