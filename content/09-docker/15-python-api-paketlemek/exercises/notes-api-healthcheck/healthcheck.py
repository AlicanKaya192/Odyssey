import os
import sys
import urllib.request

PORT = os.environ.get("PORT", "8000")

try:
    urllib.request.urlopen(f"http://localhost:{PORT}/health", timeout=2)
except OSError:
    sys.exit(1)
