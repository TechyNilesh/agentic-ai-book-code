"""
Chapter 10 - Checkpointers in LangGraph

Three checkpointer flavours: InMemorySaver, SqliteSaver, PostgresSaver.
This file is illustrative, as in the book -- it shows how to create each
saver and pass it to compile(). It assumes you already have a StateGraph
`builder` (see 03_minimal_persistent_graph.py for a full runnable graph).

Install:
    pip install langgraph
    pip install langgraph-checkpoint-sqlite     # for SqliteSaver
    pip install langgraph-checkpoint-postgres   # for PostgresSaver

Postgres connection string should come from an environment variable in
real projects -- never hardcode credentials.
"""

import os


def build_inmemory_checkpointer():
    from langgraph.checkpoint.memory import InMemorySaver
    return InMemorySaver()


def build_sqlite_checkpointer(db_path: str = "agent.db"):
    from langgraph.checkpoint.sqlite import SqliteSaver
    return SqliteSaver.from_conn_string(db_path)


def build_postgres_checkpointer():
    from langgraph.checkpoint.postgres import PostgresSaver

    conn_string = os.environ["POSTGRES_CONN_STRING"]
    checkpointer = PostgresSaver.from_conn_string(conn_string)
    checkpointer.setup()  # create tables on first run
    return checkpointer


if __name__ == "__main__":
    # Illustrative only: `builder` is your compiled StateGraph builder.
    # graph = builder.compile(checkpointer=build_sqlite_checkpointer())
    print("See 03_minimal_persistent_graph.py for a runnable example.")
