"""Chapter 12 - Worked Example: an LLM-as-judge pairwise eval.

Compares two systems (e.g. two prompt versions of a research crew) on
the same queries, using a judge model. Each query is judged twice with
the answer order swapped, which mitigates position bias.

Env vars needed:
    ANTHROPIC_API_KEY   - your Anthropic API key
    LANGSMITH_API_KEY   - optional, only needed if LANGSMITH_TRACING=true

Run:
    python 04_pairwise_llm_judge.py
"""
import json
import os

from langsmith import traceable
from langchain_anthropic import ChatAnthropic

judge = ChatAnthropic(model="claude-opus-4-7")

RUBRIC = """Score the response from 1 to 5 on accuracy, completeness,
and citation quality. Return JSON: {"winner": "A"|"B"|"tie",
"reason": "..."}."""


@traceable(name="pairwise_judge")
def pairwise(query, a, b):
    prompt = f"Q: {query}\n\nA:\n{a}\n\nB:\n{b}\n\n{RUBRIC}"
    return judge.invoke(prompt).content


def parse_winner(judge_response: str) -> str:
    """Minimal glue not shown in the book: parse the judge's JSON reply
    into "A", "B", or "tie". Falls back to "tie" if parsing fails."""
    try:
        data = json.loads(judge_response)
        return data.get("winner", "tie")
    except (json.JSONDecodeError, AttributeError):
        return "tie"


def evaluate(queries, system_a, system_b):
    wins_a = wins_b = ties = 0
    for q in queries:
        out_a, out_b = system_a(q), system_b(q)
        r1 = pairwise(q, out_a, out_b)   # A first
        r2 = pairwise(q, out_b, out_a)   # B first (swap)
        for r in (r1, r2):
            w = parse_winner(r)
            if w == "A":
                wins_a += 1
            elif w == "B":
                wins_b += 1
            else:
                ties += 1
    return wins_a, wins_b, ties


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running this script.")

    # Two toy "systems" standing in for the Chapter 8 research crew with
    # two different prompt versions.
    def system_a(query):
        return judge.invoke(f"Answer briefly: {query}").content

    def system_b(query):
        return judge.invoke(f"Answer in detail with citations: {query}").content

    demo_queries = [
        "What is the capital of India?",
        "Summarise the causes of monsoon failure in one paragraph.",
    ]
    print(evaluate(demo_queries, system_a, system_b))
