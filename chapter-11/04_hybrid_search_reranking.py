"""
Chapter 11 - Hybrid Search and Re-ranking

After retrieval, a cross-encoder re-ranker reads each (query, chunk)
pair together and gives a relevance score. Slow but accurate -- use it
on the top 20-50 candidates, then keep the top 4-6.

This is the book's fragment, wrapped with a tiny list of candidate
documents so it runs standalone.

Setup:
    pip install sentence-transformers langchain-core

Run:
    python 04_hybrid_search_reranking.py
"""

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query: str, candidates: list[Document], top_n: int = 5) -> list[Document]:
    pairs = [(query, c.page_content) for c in candidates]
    scores = reranker.predict(pairs)
    top = [c for _, c in sorted(zip(scores, candidates), reverse=True)][:top_n]
    return top


if __name__ == "__main__":
    query = "Adam optimizer"
    candidates = [
        Document(page_content="SGD with momentum is a classic optimizer."),
        Document(page_content="Adam combines momentum and adaptive learning rates."),
        Document(page_content="Gradient descent updates weights using the gradient."),
        Document(page_content="Adam is widely used for training deep networks."),
    ]
    top = rerank(query, candidates, top_n=2)
    for c in top:
        print(c.page_content)
