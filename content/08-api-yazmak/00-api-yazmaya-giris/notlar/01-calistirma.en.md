Setting up and running a FastAPI application on your own computer, and the
errors you meet most often.

## Setup

```text
python -m venv .venv
.venv\Scripts\activate
python -m pip install fastapi uvicorn
```

A virtual environment (the Packages and Environments section of the Python
track) keeps each project's packages separate. In Odyssey these packages
are ready; you do not need to install them.

## Run commands

| Command | What does it do? |
|---|---|
| `uvicorn main:app` | Opens `app` in `main.py` on 127.0.0.1:8000. |
| `uvicorn main:app --reload` | Restarts when the file is saved (while developing). |
| `uvicorn main:app --port 8001` | Another port. |
| `uvicorn main:app --host 0.0.0.0` | Other devices on the same network can reach it too (use with care). |
| `Ctrl+C` | Stops the server. |

Addresses:

| Address | What is there? |
|---|---|
| `http://127.0.0.1:8000/` | Your endpoints |
| `http://127.0.0.1:8000/docs` | Swagger UI: docs + "Try it out" |
| `http://127.0.0.1:8000/redoc` | ReDoc: a reading view of the same docs |
| `http://127.0.0.1:8000/openapi.json` | The description for machines |

## Common errors (measured)

| Message | Cause | Fix |
|---|---|---|
| `Could not import module "mian"` | The file name is misspelt or you are in another folder | Check the name in `main:app` and the folder |
| `Attribute "api" not found in module "main"` | The application object has a different name | Write it the same as `app = FastAPI()` |
| `[Errno 10048] error while attempting to bind on address` | The port is taken (another server is open) | Close the old one or use `--port 8001` |
| `{"detail":"Not Found"}` | There is no endpoint at that address | Compare the path with the address in the decorator |
| `{"detail":"Method Not Allowed"}` | The address exists but the method differs | `@app.get` / `@app.post` |

## Starting the server at the end of the code

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

Then `python main.py` also starts the server. Odyssey does not run this
line; the check calls the application without a server.
