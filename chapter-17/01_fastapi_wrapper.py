"""
Chapter 16 -- Deployment and Production

Wrapping a compiled LangGraph object in a FastAPI app (Section 16.2,
"Wrapping a Graph in FastAPI / LangServe").

NOTE: `my_agent.graph` is illustrative -- the book does not define
this module. Point the import at your own compiled LangGraph graph
(for example, the Chapter 7 personal-assistant agent or the Chapter
4 ReAct agent) before running this file.

Run locally:
    uvicorn 01_fastapi_wrapper:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel
from my_agent import graph  # your compiled LangGraph -- illustrative import

app = FastAPI()


class Query(BaseModel):
    question: str
    thread_id: str


@app.post("/chat")
def chat(q: Query):
    config = {"configurable": {"thread_id": q.thread_id}}
    result = graph.invoke({"input": q.question}, config)
    return {"answer": result["output"]}


@app.get("/health")
def health():
    return {"status": "ok"}
