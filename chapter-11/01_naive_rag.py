"""
Chapter 11 - Naive RAG

A minimal RAG pipeline: chunk a text file, embed the chunks, store them
in Chroma, retrieve the top-k chunks for a question, and ask the LLM to
answer using them.

Reads the OpenAI API key from the OPENAI_API_KEY environment variable
(langchain_openai picks this up automatically -- never hardcode it).

Setup:
    pip install langchain-chroma langchain-openai langchain-text-splitters \
                langchain-core
    export OPENAI_API_KEY=sk-...
    Create a notes.txt file in this folder with some course notes text.

Run:
    python 01_naive_rag.py
"""

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

text = open("notes.txt").read()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = [Document(page_content=c) for c in splitter.split_text(text)]

emb = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma.from_documents(docs, emb, collection_name="notes")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def naive_rag(question: str) -> str:
    chunks = store.similarity_search(question, k=4)
    context = "\n\n".join(c.page_content for c in chunks)
    prompt = f"Use the context to answer.\n\nContext:\n{context}\n\nQ: {question}"
    return llm.invoke(prompt).content


if __name__ == "__main__":
    print(naive_rag("What is a transformer block?"))
