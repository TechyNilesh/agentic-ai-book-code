"""
Chapter 3: Prompt templates -- ChatPromptTemplate and partial().

A prompt template is a reusable string with placeholders. It can
carry multiple roles (system, human, assistant) and be partially
filled when one variable is fixed for the whole application.

Setup:
    pip install -r requirements.txt

Run:
    python 02_prompt_templates.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient tutor for Indian engineering students."),
    ("human", "Explain {topic} in {language} using a simple analogy."),
])


def main() -> None:
    messages = prompt.invoke(
        {"topic": "gradient descent", "language": "Hindi"}
    )
    for m in messages.to_messages():
        print(m.type, "->", m.content[:60])

    # Partial templates: fix one variable for the whole application.
    tutor = prompt.partial(language="English")
    print(tutor.invoke({"topic": "attention"}).to_messages()[1].content)


if __name__ == "__main__":
    main()
