"""
Chapter 11 - Embeddings and Vector Stores

Creates a Chroma store with on-disk persistence, as in the book.
Reads the OpenAI API key from the OPENAI_API_KEY environment variable.

Setup:
    pip install langchain-chroma langchain-openai langchain-core
    export OPENAI_API_KEY=sk-...

Run:
    python 03_embeddings_vector_store.py
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

emb = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma(
    collection_name="course_notes",
    embedding_function=emb,
    persist_directory="./chroma_db")


if __name__ == "__main__":
    docs = [
        Document(page_content="Transformers use self-attention layers."),
        Document(page_content="RNNs process sequences one step at a time."),
    ]
    store.add_documents(docs)
    results = store.similarity_search("attention mechanism", k=1)
    for r in results:
        print(r.page_content)
