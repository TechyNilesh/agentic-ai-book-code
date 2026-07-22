"""
Chapter 15 -- Comparative Frameworks: Beyond LangGraph

Pydantic AI: an agent whose input and output are validated Pydantic
models (Section 15.6, "Pydantic AI and Semantic Kernel").

Set your API key:

    export OPENAI_API_KEY=sk-...

Run:
    python 05_pydantic_ai.py
"""

from pydantic_ai import Agent
from pydantic import BaseModel


class Answer(BaseModel):
    summary: str
    confidence: float


agent = Agent("openai:gpt-4o", result_type=Answer)

if __name__ == "__main__":
    result = agent.run_sync(
        "Summarise the theory of relativity in 30 words."
    )
    print(result.data.summary, result.data.confidence)
