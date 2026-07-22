"""
Chapter 11 - Chunking Strategies

The RecursiveCharacterTextSplitter tries large separators first
(paragraphs, then sentences, then words), which keeps related text
together better than a fixed-size cut.

Setup:
    pip install langchain-text-splitters

Run:
    python 02_chunking_strategies.py
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def recursive_chunk(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " ", ""])
    return splitter.split_text(text)


if __name__ == "__main__":
    sample = (
        "Photosynthesis is the process by which green plants use sunlight, "
        "water, and carbon dioxide to produce glucose and oxygen.\n\n"
        "Chlorophyll in the chloroplasts absorbs light, mainly in blue and "
        "red. The Calvin cycle fixes CO2 into sugars in the stroma."
    )
    chunks = recursive_chunk(sample)
    for i, c in enumerate(chunks, 1):
        print(f"--- chunk {i} ---")
        print(c)
