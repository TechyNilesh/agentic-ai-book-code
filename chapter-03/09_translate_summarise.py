"""
Chapter 3, Solved Problem 3.1: Translate then summarise.

A single LCEL chain that takes English text, translates it to
Hindi, and then summarises the Hindi text into three bullets.
RunnableLambda adapts the string output of stage one into the dict
input of stage two.

Setup:
    pip install -r requirements.txt

Run:
    python 09_translate_summarise.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

load_dotenv()

llm = init_chat_model("anthropic:claude-sonnet-4-6")
parse = StrOutputParser()

translate = (
    ChatPromptTemplate.from_template(
        "Translate to Hindi:\n{text}")
    | llm | parse
)
summarise = (
    ChatPromptTemplate.from_template(
        "Summarise in 3 Hindi bullet points:\n{hindi}")
    | llm | parse
)

pipeline = translate | RunnableLambda(
    lambda h: {"hindi": h}) | summarise


if __name__ == "__main__":
    print(pipeline.invoke(
        {"text": "Agentic AI lets models act, not just answer."}))
