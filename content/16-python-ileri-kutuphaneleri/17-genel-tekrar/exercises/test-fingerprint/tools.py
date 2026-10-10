import hashlib


def fingerprint(text):
    clean = text.strip().lower()
    return hashlib.sha256(clean.encode()).hexdigest()[:12]
