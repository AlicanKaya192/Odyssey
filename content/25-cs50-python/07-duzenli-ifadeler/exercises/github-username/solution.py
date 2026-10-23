import re

url = input("URL: ").strip()

if matches := re.search(r"^(?:https?://)?(?:www\.)?github\.com/([a-z0-9-]+)", url, re.IGNORECASE):
    print(f"Username: {matches.group(1)}")
else:
    print("Not a GitHub profile")
