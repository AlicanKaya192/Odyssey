import os

env = os.environ.get("APP_ENV", "development")
port = int(os.environ.get("PORT", "8000"))
print("env:", env, "port:", port + 0)
