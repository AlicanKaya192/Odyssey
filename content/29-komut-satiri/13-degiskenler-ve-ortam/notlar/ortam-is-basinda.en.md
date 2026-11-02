Environment variables are the way to give a program settings **without
changing its code**. A few of them that you also meet in the other paths:

## Variables that programs read

| Variable | Who reads it | What it is for |
|---|---|---|
| `EDITOR` | git and other programs | Which editor to open |
| `PATH` | The shell | The folders where commands are looked for |
| `HOME` | Almost every program | Where settings files are |
| `LANG` | Most programs | Language and character encoding |
| `LC_ALL=C` | sort and similar tools | The same sort order everywhere |
| `PYTHONPATH` | Python | Extra folders where modules are looked for |

## Do not write secrets into code

An API key or a database password is not written into the code; when the code
goes to GitHub, the secret goes with it. Instead, the program reads the value
from the environment:

```bash
export API_KEY=...        # only in your own terminal
python app.py             # the program reads it with os.environ["API_KEY"]
```

`os.environ.get("API_KEY")` in Python, `-e` and `env_file` in Docker, and
`secrets` in GitHub Actions are different spellings of the same idea. Do not
write the secret into `.bashrc` either; if you share the computer or back up
your `.bashrc`, it goes along.

## Python virtual environments and PATH

`source .venv/bin/activate` (on Windows `.venv\Scripts\activate`) actually
adds the `bin` folder of `.venv` to the front of PATH. That is why the
`python` you type afterwards is the virtual environment's Python. `which
python` shows which one you are using.

## "I installed it but it cannot be found"

1. Is `which program` empty? The program is not in PATH.
2. Find the folder the program was installed in.
3. Try `export PATH="that/folder:$PATH"`; if it works, write the line into
   `.bashrc`.
