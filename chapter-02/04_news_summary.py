"""
Chapter 2, Lab 2.1: Structured News Summariser.

Reads a news article from a text file and prints a structured
summary (headline, summary, key entities, sentiment, topic).

Setup:
    pip install langchain langchain-anthropic pydantic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python 04_news_summary.py sample_article.txt
"""

import sys
from typing import List, Literal

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


class NewsSummary(BaseModel):
    headline: str = Field(description="<=12 words.")
    summary: str = Field(description="3-4 sentence summary.")
    key_entities: List[str] = Field(
        description="People, places, organisations."
    )
    sentiment: Literal["positive", "neutral", "negative"]
    topic: Literal[
        "politics", "business", "sports",
        "technology", "science", "other",
    ]


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        article = f.read()

    llm = init_chat_model(
        "claude-sonnet-4-6",
        model_provider="anthropic",
        temperature=0,
    )
    summariser = llm.with_structured_output(NewsSummary)

    result = summariser.invoke([
        ("system",
         "You are a precise news editor. "
         "Extract a structured summary."),
        ("user", article),
    ])
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
