"""Smart Study Assistant - entry point.

Run with:  python -m capstone1 run

Starter scaffold from Chapter 17, Lab "Starter scaffold for
Capstone 1". Fill in the TODOs in loader.py, index.py, retriever.py,
quiz.py, and scheduler.py one by one. Commit after each.
"""
import argparse
from capstone1 import index, retriever, quiz


def cmd_build(args):
    # TODO: load PDFs from data/pdfs and build the vector store
    index.build("data/pdfs", out_dir=".store")


def cmd_ask(args):
    # TODO: retrieve top-k chunks and answer with citations
    answer = retriever.answer(args.question, store=".store")
    print(answer)


def cmd_quiz(args):
    # TODO: generate 5 MCQs on the given topic
    qs = quiz.generate(args.topic, n=5, store=".store")
    for q in qs:
        print(q)


def cmd_run(args):
    # TODO: launch Streamlit UI tying it all together
    import streamlit.web.cli as stcli
    stcli.main_run(["src/capstone1/ui.py"])


def main():
    p = argparse.ArgumentParser(prog="capstone1")
    sub = p.add_subparsers(required=True)

    sub.add_parser("build").set_defaults(func=cmd_build)

    ask = sub.add_parser("ask")
    ask.add_argument("question")
    ask.set_defaults(func=cmd_ask)

    qz = sub.add_parser("quiz")
    qz.add_argument("topic")
    qz.set_defaults(func=cmd_quiz)

    sub.add_parser("run").set_defaults(func=cmd_run)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
