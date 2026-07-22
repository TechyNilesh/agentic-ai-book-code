"""
Chapter 16 -- Deployment and Production

Pointing LangChain at a local Ollama server for fully local, offline
deployment (Section 16.7, "Local Deployment with Ollama and vLLM").

Before running this, start the Ollama server in another terminal:

    ollama pull llama3.1:8b
    ollama serve   # exposes an OpenAI-compatible API on :11434

Run:
    python 03_local_ollama_llm.py
"""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # any string works
    model="llama3.1:8b",
)

if __name__ == "__main__":
    result = llm.invoke("Say hello in one short sentence.")
    print(result.content)
