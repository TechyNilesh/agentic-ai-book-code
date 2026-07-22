"""
Chapter 2: Hello world with a chat model.

Shows the provider-agnostic init_chat_model helper. Swap
model_provider="anthropic" for "openai" or "groq" and the rest
of the code stays the same.

Setup:
    pip install langchain langchain-anthropic
    export ANTHROPIC_API_KEY="sk-ant-..."

Run:
    python 01_hello_chat_model.py
"""

from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "claude-sonnet-4-6",
    model_provider="anthropic",
    temperature=0,
)


def main() -> None:
    response = llm.invoke(
        [
            ("system", "You are a concise assistant."),
            ("user", "Name the three primary colours."),
        ]
    )
    print(response.content)


if __name__ == "__main__":
    main()
