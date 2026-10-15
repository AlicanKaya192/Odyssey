import re

API_KEY = re.compile(r"apikey_[A-Za-z0-9]{20}")
PASSWORD = re.compile(r'password\s*=\s*"[^"]+"')


def find_secrets(files):
    # Dosyalari sirali gez, her satiri iki desenle dene.
    pass


files = {
    "settings.py": 'DEBUG = True\npassword = "hunter2"\n',
    "app.py": 'import os\nkey = os.environ["API_KEY"]\n',
    "old_config.py": 'KEY = "apikey_7Hq2Lm9Xc4Vb8Nz1Rt5W"\npassword = ""\n',
}
for line in find_secrets(files):
    print(line)
