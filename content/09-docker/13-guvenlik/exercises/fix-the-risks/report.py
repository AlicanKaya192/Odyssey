import getpass
import os

print("user:", getpass.getuser())
print("password set:", bool(os.environ.get("DB_PASSWORD")))
