"""Chapter 12 - Tracing with LangSmith.

Shows the minimal setup to trace a function with LangSmith: two
environment variables and the @traceable decorator. Nested LangChain
calls inside a traced function attach as child spans automatically.

Env vars needed:
    LANGSMITH_API_KEY   - your LangSmith API key
    ANTHROPIC_API_KEY   - your Anthropic API key (for the LLM call)

Run:
    python 01_langsmith_tracing.py
"""
import os

# Turn tracing on. Never hardcode the key -- read it from the environment.
os.environ["LANGSMITH_TRACING"] = "true"
os.environ.setdefault("LANGSMITH_API_KEY", os.environ.get("LANGSMITH_API_KEY", ""))
os.environ["LANGSMITH_PROJECT"] = "research-crew"

from langsmith import traceable
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-5")


@traceable(name="summarize_paper")
def summarize_paper(text: str) -> str:
    # Any LLM or tool calls inside will be nested as child spans.
    return llm.invoke(f"Summarize:\n{text}").content


if __name__ == "__main__":
    if not os.environ.get("LANGSMITH_API_KEY"):
        raise SystemExit("Set LANGSMITH_API_KEY before running this script.")
    sample_text = (
        "Agentic AI systems combine large language models with tools, "
        "memory, and planning loops to complete multi-step tasks."
    )
    print(summarize_paper(sample_text))
