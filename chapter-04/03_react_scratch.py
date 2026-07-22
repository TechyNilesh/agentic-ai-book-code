"""
Chapter 4 - Reasoning and Planning
Listings 4.3 (ReAct prompt template) and 4.4 (ReAct loop from scratch).

A hand-written ReAct loop: the code builds the prompt, calls the model,
parses the requested action, runs the tool, feeds the observation back,
and repeats until the model writes "Final Answer:".

Env vars needed:
    OPENAI_API_KEY  -- your OpenAI API key
"""

import os
import re

from langchain_openai import ChatOpenAI

REACT_PROMPT = """Answer the question using these tools:

calculator(expression): evaluate a math expression, e.g. calculator(3 * 4)

Use this exact format:

Thought: your reasoning about what to do next
Action: tool_name(arguments)
Observation: the result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the answer to the user

Question: {question}
{scratchpad}"""


def calculator(expr: str) -> str:
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"error: {e}"


TOOLS = {"calculator": calculator}


def run_react(llm: ChatOpenAI, question: str, max_steps: int = 8) -> str:
    scratchpad = ""
    for _ in range(max_steps):
        prompt = REACT_PROMPT.format(question=question, scratchpad=scratchpad)
        out = llm.invoke(prompt).content
        scratchpad += out

        if "Final Answer:" in out:
            return out.split("Final Answer:")[-1].strip()

        m = re.search(r"Action:\s*(\w+)\((.*)\)", out)
        if not m:
            return "Could not parse action."
        name, arg = m.group(1), m.group(2).strip()
        obs = TOOLS[name](arg)
        scratchpad += f"\nObservation: {obs}\n"
    return "Step limit reached."


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set the OPENAI_API_KEY environment variable first.")

    # stop=["Observation:"] makes the model halt right where a real
    # observation should appear, so our code -- not the model -- writes it.
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, stop=["Observation:"])

    print(run_react(llm, "What is 17 * 23 + 9?"))


if __name__ == "__main__":
    main()
