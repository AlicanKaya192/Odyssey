"""Pretends to read the model file from disk and counts the reads."""

reads = {"count": 0}


def read_model():
    """Read the model; every call is one slow read from the disk."""
    reads["count"] += 1
    return {"name": "churn", "version": 3}
