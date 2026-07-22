"""
Chapter 3: Callbacks and tracing.

A callback is a function the framework calls when something happens:
a chain starts, a token is produced, an error is raised. For
production, LangSmith records every step instead of hand-written
callbacks -- set the environment variables shown below.

Setup:
    pip install -r requirements.txt
    # Optional, for hosted tracing:
    export LANGSMITH_TRACING=true
    export LANGSMITH_API_KEY=lsv2_...
    export LANGSMITH_PROJECT=agentic-book

Run:
    python 07_callbacks.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

claude = init_chat_model("anthropic:claude-sonnet-4-6")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a patient tutor for Indian engineering students."),
    ("human", "Explain {topic} in {language} using a simple analogy."),
])

chain = prompt | claude | StrOutputParser()


class TraceHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kw):
        print(">> LLM start, prompt[0]:", prompts[0][:60])

    def on_llm_end(self, response, **kw):
        print(">> LLM end")


def main() -> None:
    chain.invoke(
        {"topic": "GANs", "language": "English"},
        config={"callbacks": [TraceHandler()]},
    )


if __name__ == "__main__":
    main()
