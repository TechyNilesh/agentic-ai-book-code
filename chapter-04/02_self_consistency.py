"""
Chapter 4 - Reasoning and Planning
Listing 4.2: Self-consistency with k samples.

Run the same Chain-of-Thought prompt k times at a non-zero temperature,
extract the final number from each run, and vote for the most common
answer. This trades extra API calls for higher accuracy.

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
import re
from collections import Counter

from langchain_openai import ChatOpenAI


def extract_final(text: str) -> str | None:
    nums = re.findall(r"-?\d+(?:\.\d+)?", text)
    return nums[-1] if nums else None


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    prompt = (
        "A trader buys 240 mangoes at Rs. 8 each. He sells 150 at "
        "Rs. 12 each and the rest at Rs. 6 each. What is the profit "
        "or loss? Let's think step by step."
    )

    answers = [extract_final(llm.invoke(prompt).content) for _ in range(5)]
    print("All answers:", answers)
    print("Voted answer:", Counter(answers).most_common(1)[0][0])


if __name__ == "__main__":
    main()
