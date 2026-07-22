"""
Chapter 2: Worked Example -- Extracting Structured Data from a Review.

Turns one unstructured customer review into a database-ready row
using a richer Pydantic schema (lists, inferred star rating, etc.).

Setup:
    pip install langchain langchain-anthropic pydantic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python 03_review_extractor.py
"""

from typing import List, Literal

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field


class ReviewInfo(BaseModel):
    product_name: str
    sentiment: Literal["positive", "negative", "neutral"]
    star_rating_inferred: int = Field(ge=1, le=5)
    complaints: List[str]
    compliments: List[str]


llm = init_chat_model(
    "claude-sonnet-4-6", model_provider="anthropic", temperature=0
)
extractor = llm.with_structured_output(ReviewInfo)

review = (
    "I bought the Acme X1 headphones last week. "
    "Sound quality is amazing, bass is deep. "
    "But the battery dies in 3 hours. Disappointing."
)


def main() -> None:
    info = extractor.invoke(review)
    print(info.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
