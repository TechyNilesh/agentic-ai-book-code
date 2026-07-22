"""
Chapter 10 - Encrypted Serializers

By default LangGraph serialises state using JSON or pickle -- plaintext
on disk. For sensitive data (PII, medical records, payment details),
wrap the checkpointer's serde with EncryptedSerializer.

This is illustrative, as in the book. It needs a real encryption key
supplied via the LG_ENCRYPTION_KEY environment variable -- never
hardcode it, and never check it into version control. Keep it in a
secrets manager (AWS Secrets Manager, HashiCorp Vault) in production.

Run (after exporting LG_ENCRYPTION_KEY):
    python 05_encrypted_serializer.py
"""

import os

from langgraph.checkpoint.serde.encrypted import EncryptedSerializer
from langgraph.checkpoint.sqlite import SqliteSaver


def build_encrypted_sqlite_saver(db_path: str = "private.db"):
    key = os.environ["LG_ENCRYPTION_KEY"]  # 32 random bytes, base64
    serde = EncryptedSerializer.from_pycryptodome_aes(key)

    saver = SqliteSaver.from_conn_string(db_path)
    saver.serde = serde
    return saver


if __name__ == "__main__":
    if "LG_ENCRYPTION_KEY" not in os.environ:
        print("Set LG_ENCRYPTION_KEY to a base64-encoded 32-byte key first.")
    else:
        saver = build_encrypted_sqlite_saver()
        print("Encrypted saver ready:", saver)
        # graph = builder.compile(checkpointer=saver)
