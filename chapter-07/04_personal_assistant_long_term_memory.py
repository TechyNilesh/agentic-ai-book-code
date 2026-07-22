"""
Chapter 7 - Memory in Agentic Systems
Lab 7.1: A personal assistant with episodic long-term memory.

Every user message and assistant reply is saved as an episode in
Chroma. On each new query, the top-3 relevant past episodes are
retrieved and injected into the system prompt, so the assistant
remembers facts across turns -- and across separate runs of this
script, since Chroma persists to disk.

Setup:
    pip install langgraph langchain-openai langchain-chroma chromadb
    export OPENAI_API_KEY=sk-...
"""

import os
from datetime import datetime

from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

emb = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
mem = Chroma(
    persist_directory="./assistant_mem",
    embedding_function=emb,
    collection_name="episodes",
)


def save_episode(user_id: str, text: str) -> None:
    mem.add_texts(
        [text], metadatas=[{"user": user_id, "ts": datetime.utcnow().isoformat()}]
    )


def recall(user_id: str, query: str, k: int = 3):
    hits = mem.similarity_search(query, k=k, filter={"user": user_id})
    return [h.page_content for h in hits]


def chat(user_id: str, user_msg: str) -> str:
    past = recall(user_id, user_msg)
    context = "\n".join(f"- {p}" for p in past) or "(no prior notes)"
    sys = (
        "You are a helpful personal assistant. "
        "Use these notes about the user:\n" + context
    )
    reply = llm.invoke(
        [SystemMessage(content=sys), HumanMessage(content=user_msg)]
    ).content
    save_episode(user_id, f"User said: {user_msg}")
    save_episode(user_id, f"Assistant said: {reply}")
    return reply


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    uid = "aarav"
    for turn in [
        "Hi, I'm Aarav. I'm vegetarian.",
        "I am allergic to peanuts too.",
        "Suggest a quick evening snack.",
        "What is my name?",
        "Plan a 3-day dinner menu for me.",
    ]:
        print(">>", turn)
        print(chat(uid, turn))
        print()


if __name__ == "__main__":
    main()
