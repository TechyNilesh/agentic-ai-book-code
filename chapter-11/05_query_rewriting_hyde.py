"""
Chapter 11 - Query Rewriting: HyDE

HyDE (Hypothetical Document Embeddings): ask the LLM to write a fake
but plausible answer first, then embed that fake answer and retrieve
real chunks near it. Answer-like text matches answer-like chunks
better than a short question does.

Reads the OpenAI API key from the OPENAI_API_KEY environment variable.

Setup:
    pip install langchain-openai
    export OPENAI_API_KEY=sk-...

Run:
    python 05_query_rewriting_hyde.py
"""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def hyde(question: str) -> str:
    p = f"Write a one-paragraph answer to: {question}"
    return llm.invoke(p).content


if __name__ == "__main__":
    print(hyde("How does backpropagation work?"))
