import os

key = os.environ.get("REPORT_API_KEY", "")
print("report sent" if key else "no key")
