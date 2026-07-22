"""
Chapter 1, Lab 1, Step 4: A hello-world LLM call.

Setup:
    pip install langchain-anthropic anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python hello_llm.py
"""

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=200)


def main() -> None:
    reply = llm.invoke("In one sentence, what is an AI agent?")
    print(reply.content)


if __name__ == "__main__":
    main()
