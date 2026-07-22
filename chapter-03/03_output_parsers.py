"""
Chapter 3: Three common output parsers.

The model returns an AIMessage object. Output parsers convert that
into plain text, free-form JSON, or a typed Pydantic object.

Setup:
    pip install -r requirements.txt

Run:
    python 03_output_parsers.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import (
    JsonOutputParser,
    StrOutputParser,
)
from pydantic import BaseModel, Field

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

# 1. Plain string
str_parser = StrOutputParser()

# 2. Free-form JSON
json_parser = JsonOutputParser()


# 3. Typed Pydantic output via with_structured_output
class Recipe(BaseModel):
    dish: str = Field(description="Name of the dish")
    steps: list[str] = Field(description="Cooking steps")
    minutes: int


structured_model = claude.with_structured_output(Recipe)


def main() -> None:
    r = structured_model.invoke(
        "Give me a 4-step recipe for masala chai."
    )
    print(r.dish, r.minutes, r.steps)


if __name__ == "__main__":
    main()
