"""Capstone 1 -- vector store build.

Part of the starter scaffold in Chapter 17. `app.py` calls
`index.build(pdf_dir, out_dir)`. Not printed in the book; implement
this using loader.py's chunks and a vector store such as Chroma (see
Chapter 8, "Vector stores and embeddings").
"""


def build(pdf_dir: str, out_dir: str = ".store") -> None:
    # TODO: load + chunk PDFs from pdf_dir (see loader.py) and write
    # embeddings to a persistent vector store at out_dir.
    raise NotImplementedError("Fill this in -- see Chapters 7-8.")
