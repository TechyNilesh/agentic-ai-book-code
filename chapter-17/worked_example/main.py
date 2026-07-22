"""
Chapter 16 -- Deployment and Production

Worked Example: Dockerising a 2-Tool Agent (Section 16.9). A small
LangGraph ReAct agent with a calculator tool and a Wikipedia-search
tool, wrapped in FastAPI.

NOTE: `tools.py` (the `calculator` and `wiki_search` tools) is
illustrative -- the book does not print their source. Write your own
`tools.py` in this folder, exposing two LangChain `@tool`-decorated
functions named `calculator` and `wiki_search`, before running this
app. See Chapter 5 for tool-definition patterns.

Run locally:
    uvicorn main:app --reload --port 8000

Or via Docker (see Dockerfile in this folder):
    docker build -t two-tool-agent .
    docker run -p 8000:8000 -e OPENAI_API_KEY=$KEY two-tool-agent
    curl -X POST localhost:8000/ask \\
         -H "Content-Type: application/json" \\
         -d '{"q": "What is 13*19?"}'
"""

from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tools import calculator, wiki_search  # illustrative -- write these yourself

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_react_agent(llm, [calculator, wiki_search])

app = FastAPI()


class Q(BaseModel):
    q: str


@app.post("/ask")
def ask(body: Q):
    out = agent.invoke({"messages": [("user", body.q)]})
    return {"answer": out["messages"][-1].content}


@app.get("/health")
def health():
    return {"ok": True}
