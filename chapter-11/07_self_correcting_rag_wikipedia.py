"""
Chapter 11 - Worked Example: A Self-Correcting RAG on a Wikipedia
Snippet

A small CRAG-style graph over a single Wikipedia paragraph about
photosynthesis: retrieve, grade the chunks, rewrite the query if the
grade is poor, and generate an answer once the grade is good (or after
two tries).

Reads the OpenAI API key from the OPENAI_API_KEY environment variable.

Setup:
    pip install langgraph langchain-chroma langchain-openai langchain-core
    export OPENAI_API_KEY=sk-...

Run:
    python 07_self_correcting_rag_wikipedia.py
"""

from typing import TypedDict, List

from langgraph.graph import StateGraph, END
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

snippet = (
 "Photosynthesis is the process by which green plants use sunlight, "
 "water, and carbon dioxide to produce glucose and oxygen. "
 "Chlorophyll in the chloroplasts absorbs light, mainly in blue and red. "
 "The Calvin cycle fixes CO2 into sugars in the stroma.")

docs = [Document(page_content=s.strip()) for s in snippet.split(". ") if s]
emb = OpenAIEmbeddings(model="text-embedding-3-small")
store = Chroma.from_documents(docs, emb, collection_name="bio")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class S(TypedDict):
    question: str
    chunks: List[Document]
    grade: str
    answer: str
    tries: int


def retrieve(s: S) -> S:
    s["chunks"] = store.similarity_search(s["question"], k=2)
    return s


def grade(s: S) -> S:
    ctx = "\n".join(c.page_content for c in s["chunks"])
    p = (f"Question: {s['question']}\nChunks:\n{ctx}\n"
         "Are the chunks relevant? Reply only YES or NO.")
    s["grade"] = llm.invoke(p).content.strip().upper()
    return s


def rewrite(s: S) -> S:
    p = f"Rewrite this query to be clearer: {s['question']}"
    s["question"] = llm.invoke(p).content
    s["tries"] = s.get("tries", 0) + 1
    return s


def generate(s: S) -> S:
    ctx = "\n".join(c.page_content for c in s["chunks"])
    p = f"Answer using context.\nContext:\n{ctx}\nQ: {s['question']}"
    s["answer"] = llm.invoke(p).content
    return s


def decide(s: S) -> str:
    if "YES" in s["grade"] or s.get("tries", 0) >= 2:
        return "generate"
    return "rewrite"


g = StateGraph(S)
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
app = g.compile()


if __name__ == "__main__":
    print(app.invoke({"question": "What gas does photosynthesis release?",
                      "tries": 0})["answer"])
    print(app.invoke({"question": "How do plants make food?",
                      "tries": 0})["answer"])
