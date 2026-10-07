Check before putting a model live behind an API.

## Loading

- ☐ The model is loaded **once** in `lifespan`, not in the endpoint.
- ☐ What's saved is the whole pipeline, not just the model.
- ☐ The scikit-learn version is pinned in `requirements.txt`.

## Input

- ☐ Every feature is in the Pydantic model, with its type and a sensible
  range (`Field(gt=0, le=10)`).
- ☐ The column order matches training (in one helper function, one place).
- ☐ Batch prediction has a limit on the list size
  (`if len(flowers) > 100:` → an error): nobody should send 10 million rows.

## Output

- ☐ NumPy values are converted with `int()`, `float()`, `.tolist()`.
- ☐ A readable name (`"setosa"`) instead of a class number, with a
  probability if needed.
- ☐ A `/model` endpoint: the model type, version, classes.

## Behaviour

- ☐ The prediction endpoint is `def` (scikit-learn does blocking
  calculation; inside `async def` it locks the event loop).
- ☐ Tests: a few known examples get the right class, broken input is
  `422`.

## Common mistakes (measured)

| Mistake | Result |
|---|---|
| Returning a NumPy value directly | `500` |
| Forgetting the scaler | No error, every prediction the same class |
| Giving one example as a flat list (`[5.1, 3.5, ...]`) | scikit-learn `Expected 2D array` |
