"""
Chapter 7 - Memory in Agentic Systems
Listing: Embed and store with Chroma.

A vector store lets an agent find relevant past episodes by meaning,
not exact words, using cosine similarity between embeddings.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    emb = OpenAIEmbeddings(model="text-embedding-3-small")
    store = Chroma(
        persist_directory="./mem_db",
        embedding_function=emb,
        collection_name="episodes",
    )
    store.add_texts(
        ["User Aarav is vegetarian."], metadatas=[{"user": "aarav"}]
    )
    hits = store.similarity_search("what can Aarav eat?", k=3)
    for h in hits:
        print(h.page_content, h.metadata)


if __name__ == "__main__":
    main()
