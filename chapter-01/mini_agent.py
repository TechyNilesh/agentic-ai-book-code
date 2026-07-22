"""
Chapter 1, Lab 1, Step 5: A one-shot mini-agent that greets or computes.

It reads a user message, asks the LLM to pick an action (greet or
compute), and then runs the matching Python function. The LLM does
not do the arithmetic itself -- it only picks the tool and the
argument. That is the smallest possible agent.

Setup:
    pip install langchain-anthropic anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python mini_agent.py
"""

import json

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=300)

ROUTER_PROMPT = """You are a router. Read the user message and
reply with ONLY a JSON object of the form:
{{"action": "greet"}}  or  {{"action": "compute", "expr": "..."}}

Use "greet" for hellos and small talk.
Use "compute" for any arithmetic question; put the bare
expression in "expr", e.g. "23 * 7 + 4".

User message: {msg}
JSON:"""


def greet():
    return "Hello! I am a tiny agent. Ask me to add or multiply."


def compute(expr: str):
    allowed = set("0123456789+-*/(). ")
    if not set(expr) <= allowed:
        return "Refusing to evaluate: unsafe characters."
    return f"{expr} = {eval(expr)}"


def run(user_msg: str):
    raw = llm.invoke(ROUTER_PROMPT.format(msg=user_msg)).content
    plan = json.loads(raw.strip())
    if plan["action"] == "greet":
        return greet()
    if plan["action"] == "compute":
        return compute(plan["expr"])
    return "I do not know what to do."


if __name__ == "__main__":
    print(run("hi there"))
    print(run("what is 23 times 7 plus 4?"))
