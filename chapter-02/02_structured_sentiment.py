"""
Chapter 2: Structured output with Pydantic v2.

Instead of parsing free-form text, we ask the model to fill a
Pydantic schema. LangChain validates the result for us via
with_structured_output.

Setup:
    pip install langchain langchain-anthropic pydantic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python 02_structured_sentiment.py
"""

from typing import Literal

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


class Sentiment(BaseModel):
    """Sentiment analysis of a single review."""

    label: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = Field(description="One short sentence.")


llm = init_chat_model(
    "claude-sonnet-4-6", model_provider="anthropic", temperature=0
)
classifier = llm.with_structured_output(Sentiment)


def main() -> None:
    result = classifier.invoke(
        "The food was great but service was slow."
    )
    print(result.label, result.confidence)
    print(result.reason)


if __name__ == "__main__":
    main()
