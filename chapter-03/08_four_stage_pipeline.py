"""
Chapter 3, Worked Example / Lab 3 base: a four-stage article pipeline.

Stages: (1) outline the topic, (2) write a draft from the outline,
(3) critique the draft, (4) rewrite the draft fixing the weaknesses.
Each stage is a small, testable LCEL chain; the orchestration between
stages is plain Python.

This is the same pipeline shape Lab 3 asks you to extend with a
translate-to-Hindi and summarise stage (see the lab instructions in
the book and README.md in this folder).

Setup:
    pip install -r requirements.txt

Run:
    python 08_four_stage_pipeline.py
"""

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = init_chat_model("anthropic:claude-sonnet-4-6")
parse = StrOutputParser()

outline_p = ChatPromptTemplate.from_template(
    "Give a 5-point outline for an article on: {topic}")
write_p = ChatPromptTemplate.from_template(
    "Write a 200-word article from this outline:\n{outline}")
critique_p = ChatPromptTemplate.from_template(
    "List 3 weaknesses of this draft:\n{draft}")
finalise_p = ChatPromptTemplate.from_template(
    "Rewrite the draft fixing these weaknesses.\n"
    "Draft:\n{draft}\n\nWeaknesses:\n{weaknesses}")

outline = outline_p | llm | parse
write = write_p | llm | parse
critique = critique_p | llm | parse


def run(topic: str) -> str:
    o = outline.invoke({"topic": topic})
    d = write.invoke({"outline": o})
    w = critique.invoke({"draft": d})
    return (finalise_p | llm | parse).invoke(
        {"draft": d, "weaknesses": w})


if __name__ == "__main__":
    print(run("Why agentic AI matters for Indian startups"))
