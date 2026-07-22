"""
Chapter 7 - Memory in Agentic Systems
Listing: LangGraph's store API.

LangGraph (v1.0) ships a BaseStore interface for long-term memory.
InMemoryStore is the simplest implementation; production systems
typically use Postgres or a vector backend instead.

Env vars needed: none.
"""

from langgraph.store.memory import InMemoryStore


def main() -> None:
    store = InMemoryStore()
    ns = ("user_123", "episodes")
    store.put(
        ns, key="ep1", value={"text": "Aarav is vegetarian", "ts": "2026-05-10"}
    )
    items = store.search(ns, query="diet", limit=5)
    for item in items:
        print(item)


if __name__ == "__main__":
    main()
