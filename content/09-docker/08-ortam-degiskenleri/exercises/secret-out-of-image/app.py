import os
import sys

key = os.environ.get("API_KEY")
if not key:
    sys.exit("API_KEY is not set")
print("key loaded:", len(key), "chars")
