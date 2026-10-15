import sys
import time
import urllib.request

url = sys.argv[1].rstrip("/") + "/health"
for attempt in range(1, 6):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                print(f"healthy after {attempt} attempt(s)")
                sys.exit(0)
    except OSError:
        pass
    time.sleep(2 * attempt)
print("not healthy")
sys.exit(1)
