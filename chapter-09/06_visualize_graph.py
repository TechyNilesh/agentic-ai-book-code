"""
Chapter 9 - Visualising a Graph

Once a graph is compiled, you can ask it for a drawing (Mermaid PNG or
Mermaid source). This reuses the counter graph from 01_counter_graph.py.

Run:
    python 06_visualize_graph.py
"""

def get_counter_graph():
    # Import here (rather than at module load) so this file can be run
    # directly with `python 06_visualize_graph.py` from this folder.
    import importlib.util
    import pathlib

    module_path = pathlib.Path(__file__).parent / "01_counter_graph.py"
    spec = importlib.util.spec_from_file_location("counter_graph", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.graph


if __name__ == "__main__":
    graph = get_counter_graph()

    # Mermaid source (always works, no extra dependencies)
    print(graph.get_graph().draw_mermaid())

    # Mermaid PNG (requires internet access / extra deps in some setups)
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_bytes)
        print("Wrote graph.png")
    except Exception as exc:  # pragma: no cover - illustrative only
        print(f"Could not render PNG: {exc}")
