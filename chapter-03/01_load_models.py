"""
Chapter 3: Loading models from four different providers.

init_chat_model is the provider-agnostic loader. Every model it
returns exposes the same interface: .invoke(), .stream(),
.ainvoke(), .astream(), .batch().

Setup:
    pip install -r requirements.txt
    Put ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY
    in a .env file (only the ones you plan to use).

Run:
    python 01_load_models.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Anthropic
claude = init_chat_model("anthropic:claude-sonnet-4-6")

# OpenAI
gpt = init_chat_model("openai:gpt-4o-mini")

# Google
gemini = init_chat_model("google_genai:gemini-1.5-flash")

# Groq (very fast Llama hosting)
llama = init_chat_model("groq:llama-3.1-70b-versatile")


def main() -> None:
    # Only claude is called here so the script runs with just an
    # ANTHROPIC_API_KEY set. Uncomment the others once you have
    # keys for those providers.
    reply = claude.invoke("In one line, what is an agent?")
    print(reply.content)


if __name__ == "__main__":
    main()
