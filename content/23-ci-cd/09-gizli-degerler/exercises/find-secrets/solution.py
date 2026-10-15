import re

API_KEY = re.compile(r"apikey_[A-Za-z0-9]{20}")
PASSWORD = re.compile(r'password\s*=\s*"[^"]+"')


def find_secrets(files):
    found = []
    for name in sorted(files):
        for number, line in enumerate(files[name].splitlines(), start=1):
            if API_KEY.search(line):
                found.append(f"{name}:{number}: api-key")
            if PASSWORD.search(line):
                found.append(f"{name}:{number}: password")
    return found


files = {
    "settings.py": 'DEBUG = True\npassword = "hunter2"\n',
    "app.py": 'import os\nkey = os.environ["API_KEY"]\n',
    "old_config.py": 'KEY = "apikey_7Hq2Lm9Xc4Vb8Nz1Rt5W"\npassword = ""\n',
}
for line in find_secrets(files):
    print(line)
