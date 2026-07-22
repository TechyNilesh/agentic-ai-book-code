"""
Chapter 4 - Reasoning and Planning
Listing 4.1: Zero-shot Chain-of-Thought prompt.

Ask the model to "think step by step" instead of answering in one shot.
This alone often fixes multi-step arithmetic word problems.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os

from langchain_openai import ChatOpenAI


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    question = (
        "A trader buys 240 mangoes at Rs. 8 each. He sells 150 at "
        "Rs. 12 each and the rest at Rs. 6 each. What is the profit "
        "or loss? Let's think step by step."
    )

    print(llm.invoke(question).content)


if __name__ == "__main__":
    main()
