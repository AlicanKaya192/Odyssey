import hashlib


def evidence_status(evidence, recorded):
    lines = []
    # compute and compare each piece's hash
    return lines

import hashlib

RECORDED = {
    "image-1": hashlib.sha256("disk image one".encode()).hexdigest(),
    "image-2": hashlib.sha256("disk image two".encode()).hexdigest(),
}
EVIDENCE = {
    "image-2": "disk image 2",
    "image-1": "disk image one",
    "image-3": "memory dump",
}
for line in evidence_status(EVIDENCE, RECORDED):
    print(line)
