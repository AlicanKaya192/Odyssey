import sys

import cowsay

if len(sys.argv) != 2:
    sys.exit("Usage: python cozum.py NAME")

cowsay.cow(f"hello, {sys.argv[1]}")
