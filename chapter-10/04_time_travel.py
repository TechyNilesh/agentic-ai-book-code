"""
Chapter 10 - Time Travel: Fork and Replay

Because every super-step writes a checkpoint, the entire run history of
a thread is queryable. You can list every prior state, fork a new
branch from a past checkpoint by editing the state, or replay
deterministically for debugging.

This file re-uses the minimal counter graph from
02_minimal_persistent_graph.py so the history calls have something to
walk through.

Run:
    python 04_time_travel.py
"""

from langgraph.checkpoint.sqlite import SqliteSaver

from importlib import util
from pathlib import Path


def _load_counter_builder():
    module_path = Path(__file__).parent / "02_minimal_persistent_graph.py"
    spec = util.spec_from_file_location("counter_module", module_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.builder


if __name__ == "__main__":
    builder = _load_counter_builder()

    with SqliteSaver.from_conn_string("counter.db") as saver:
        graph = builder.compile(checkpointer=saver)
        cfg = {"configurable": {"thread_id": "demo"}}

        # Make sure there is some history to look at.
        graph.invoke({"count": 0}, config=cfg)
        graph.invoke(None, config=cfg)

        # 1. List history (newest first)
        checkpoint_ids = []
        for snap in graph.get_state_history(cfg):
            checkpoint_ids.append(snap.config["configurable"]["checkpoint_id"])
            print(snap.config["configurable"]["checkpoint_id"], snap.values)

        # 2. Pin a specific checkpoint (using the oldest one we just listed)
        target_checkpoint_id = checkpoint_ids[-1]
        target_cfg = {"configurable": {
            "thread_id": "demo",
            "checkpoint_id": target_checkpoint_id,
        }}

        # 3. Edit state at that checkpoint, then resume (forks a new branch)
        graph.update_state(target_cfg, {"count": 100})
        print(graph.invoke(None, config=target_cfg))
