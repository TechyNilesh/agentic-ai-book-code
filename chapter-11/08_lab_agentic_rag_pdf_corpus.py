"""
Chapter 11 - Lab: Agentic RAG over a Course-Notes PDF Corpus

Builds a self-correcting RAG that answers questions over a folder of
PDF lecture notes. The agent retrieves, grades, rewrites if needed,
and generates an answer with citations.

Reads the OpenAI API key from the OPENAI_API_KEY environment variable.

Setup:
    pip install langchain langgraph langchain-chroma langchain-openai \
                langchain-community pypdf
    export OPENAI_API_KEY=sk-...
    mkdir notes && cp ~/Downloads/*.pdf notes/

Run:
    python 08_lab_agentic_rag_pdf_corpus.py
"""

import os
from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# --- Step 1: Ingest PDFs ---
def ingest(notes_dir: str = "notes") -> Chroma:
    all_docs = []
    for fn in os.listdir(notes_dir):
        if fn.endswith(".pdf"):
            for d in PyPDFLoader(f"{notes_dir}/{fn}").load():
                d.metadata["source"] = fn
                all_docs.append(d)

    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=80)
    chunks = splitter.split_documents(all_docs)

    emb = OpenAIEmbeddings(model="text-embedding-3-small")
    store = Chroma.from_documents(chunks, emb,
        collection_name="course", persist_directory="./course_db")
    print(f"Indexed {len(chunks)} chunks.")
    return store


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class RAGState(TypedDict):
    question: str
    original: str
    chunks: List[Document]
    grade: str
    answer: str
    tries: int


# --- Step 2: Build the agentic RAG graph ---
def build_graph(store: Chroma):
    def retrieve(s: RAGState) -> RAGState:
        s["chunks"] = store.similarity_search(s["question"], k=5)
        return s

    def grade(s: RAGState) -> RAGState:
        ctx = "\n---\n".join(c.page_content[:300] for c in s["chunks"])
        p = (f"Question: {s['original']}\nChunks:\n{ctx}\n\n"
             "Do the chunks contain enough information to answer? "
             "Reply YES or NO.")
        s["grade"] = llm.invoke(p).content.strip().upper()
        return s

    def rewrite(s: RAGState) -> RAGState:
        p = (f"Rewrite the following question to be more specific and "
             f"include likely keywords from a textbook:\n{s['question']}")
        s["question"] = llm.invoke(p).content
        s["tries"] = s.get("tries", 0) + 1
        return s

    def generate(s: RAGState) -> RAGState:
        cites = []
        blocks = []
        for i, c in enumerate(s["chunks"], 1):
            tag = f"[{i}] {c.metadata.get('source','?')} p{c.metadata.get('page','?')}"
            cites.append(tag)
            blocks.append(f"[{i}] {c.page_content}")
        ctx = "\n\n".join(blocks)
        p = (f"Answer the question using only the context. "
             f"Cite sources as [n] inline.\n\n"
             f"Context:\n{ctx}\n\nQuestion: {s['original']}")
        s["answer"] = llm.invoke(p).content + "\n\nSources:\n" + "\n".join(cites)
        return s

    def decide(s: RAGState) -> str:
        if "YES" in s["grade"] or s.get("tries", 0) >= 2:
            return "generate"
        return "rewrite"

    g = StateGraph(RAGState)
    g.add_node("retrieve", retrieve)
    g.add_node("grade", grade)
    g.add_node("rewrite", rewrite)
    g.add_node("generate", generate)
    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "grade")
    g.add_conditional_edges("grade", decide,
        {"generate": "generate", "rewrite": "rewrite"})
    g.add_edge("rewrite", "retrieve")
    g.add_edge("generate", END)
    return g.compile()


# --- Step 3: Run a session ---
def ask(rag, q: str) -> None:
    out = rag.invoke({"question": q, "original": q, "tries": 0})
    print(out["answer"])


if __name__ == "__main__":
    store = ingest("notes")
    rag = build_graph(store)

    ask(rag, "Explain backpropagation in one paragraph.")
    ask(rag, "What is it?")  # vague; should trigger a rewrite
