"""
Chapter 5 - Tool Use and Function Calling
Defining tools in LangChain: the @tool decorator, and @tool with a
Pydantic args_schema for stricter argument control.

This file only defines the tools (as in the book) and prints their
auto-generated schemas so you can see what the LLM actually sees.

Env vars needed: none (no LLM call in this file).
"""

from pydantic import BaseModel, Field
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the product."""
    return a * b


class SearchArgs(BaseModel):
    query: str = Field(..., description="Search query in plain English.")
    max_results: int = Field(5, ge=1, le=20)


@tool(args_schema=SearchArgs)
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web and return the top results as a string."""
    # ... real implementation ...
    return f"Top {max_results} results for: {query}"


def main() -> None:
    print("multiply schema:")
    print(multiply.args_schema.model_json_schema())
    print()
    print("web_search schema:")
    print(web_search.args_schema.model_json_schema())


if __name__ == "__main__":
    main()
