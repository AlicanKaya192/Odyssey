import re


def find_secrets(source):
    pattern = re.compile(r"password\s*=\s*['\"]", re.IGNORECASE)
    found = []
    for number, line in enumerate(source.splitlines(), 1):
        if pattern.search(line):
            found.append(number)
    return found

source = """API_URL = "https://api.example.test"
SECRET_KEY = "s3cr3t-value"
password = os.environ["DB_PASSWORD"]
timeout = 30
api_token = 'abc123'"""
print(find_secrets(source))
