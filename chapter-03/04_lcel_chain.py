"""
Chapter 3: LCEL and the pipe operator.

Every prompt, model, and parser is a Runnable. Runnables are
connected with the "|" operator, same as a Unix pipe. The result is
itself a Runnable, so it can be batched, streamed, or traced.

Setup:
    pip install -r requirements.txt

Run:
    python 04_lcel_chain.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient tutor for Indian engineering students."),
    ("human", "Explain {topic} in {language} using a simple analogy."),
])

chain = prompt | claude | StrOutputParser()


def main() -> None:
    answer = chain.invoke(
        {"topic": "back-propagation", "language": "English"}
    )
    print(answer)

    # Batching and parallel calls.
    inputs = [
        {"topic": "RNN", "language": "English"},
        {"topic": "transformer", "language": "Hindi"},
        {"topic": "MLP", "language": "English"},
    ]
    results = chain.batch(inputs)  # runs in parallel
    for r in results:
        print(r[:70], "...")


if __name__ == "__main__":
    main()
