In data science and machine learning projects, the most common Git problems
are big files and secret keys. This note says what should and shouldn't go
into the repository.

## Should go in

- Code: `.py`, notebooks (`.ipynb`; better with their outputs cleared).
- Small sample data: a `sample.csv` of a few hundred rows that tests and
  lessons use.
- The recipe for the environment: `requirements.txt` or `environment.yml`.
- Documents: `README.md`, a settings **example** (`.env.example`).

## Should not go in

| What | Why | Pattern |
|---|---|---|
| Raw data | Big; the repository bloats with every change. | `data/raw/` |
| Intermediate outputs | Rebuilt from the code. | `data/processed/`, `*.parquet` |
| Trained models | Can be hundreds of MB. | `models/`, `*.pkl`, `*.joblib` |
| Virtual environment | Reinstalled on every computer. | `.venv/`, `venv/` |
| Caches | Python's and Jupyter's own files. | `__pycache__/`, `.ipynb_checkpoints/` |
| Secrets | Passwords, API keys. | `.env`, `*.key`, `credentials.json` |

## `.env` and `.env.example`

Secret settings live in `.env`, which is **ignored**. To say which settings
are needed, an example with empty values is committed:

```text
# .env.example (committed)
DATABASE_URL=
API_KEY=

# .env (ignored; the real values are here)
DATABASE_URL=postgres://...
API_KEY=sk-...
```

Someone getting the project copies `.env.example` to `.env` and fills in
their own values.

## If you really need a big file

GitHub does not accept files over 100 MB (and warns above 50 MB). For big
files there is an extension called **Git LFS** (*Large File Storage*): the
file itself lives elsewhere and the repository only holds a small text
pointing to it. For data sets it is often better not to put the data in the
repository at all and write in the README where to download it.
