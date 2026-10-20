Add a health endpoint to the model-serving service: `GET /health`, `200` and

- `{"status": "ok", "model_version": VERSION}`

`VERSION` comes from `scorer.py`; don't write it by hand.
