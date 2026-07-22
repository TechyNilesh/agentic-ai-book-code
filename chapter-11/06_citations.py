"""
Chapter 11 - Citations and Traceability

Store a unique source id in each chunk's metadata. When generating,
ask the model to attach [1], [2] markers and print a small
bibliography.

Run:
    python 06_citations.py
"""

from langchain_core.documents import Document


def build_citation_prompt(chunks: list[Document]) -> str:
    for i, c in enumerate(chunks, 1):
        c.metadata["cite"] = f"[{i}]"
    prompt = "Cite each fact with [n]. Sources:\n" + \
        "\n".join(f"[{i}] {c.page_content[:200]}" for i, c in enumerate(chunks, 1))
    return prompt


if __name__ == "__main__":
    chunks = [
        Document(page_content="Photosynthesis produces glucose and oxygen."),
        Document(page_content="Chlorophyll absorbs blue and red light."),
    ]
    print(build_citation_prompt(chunks))
