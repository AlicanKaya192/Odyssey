## Code

| Code | What it does |
|---|---|
| `joblib.dump(obj, "m.joblib")` | saves an object (model, dictionary) |
| `joblib.dump(obj, "m.joblib", compress=3)` | saves compressed |
| `joblib.load("m.joblib")` | loads it back; **can run code inside it** |
| `model.feature_names_in_` | the column names at training |
| `sklearn.__version__` | the current version |
| `InconsistentVersionWarning` | a file saved in another version |
| `warnings.simplefilter("error", InconsistentVersionWarning)` | stop on a version difference |

## Beside the model

| Key | Why |
|---|---|
| `"model"` | the whole pipeline (preprocessing included) |
| `"sklearn"`, `"python"` | the versions of the environment to load in |
| `"columns"` | the expected columns and their order |
| `"threshold"` | the chosen decision threshold (`predict` uses 0.5) |
| `"cv_auc"` or another score | the performance it was saved with |
| `"trained_at"`, `"data"` | when, with which data |

## Checklist

- Is the saved object a pipeline? If preprocessing stayed separate, the
  loaded model works wrongly on raw data.
- Are the environment's versions pinned in a `requirements.txt` file?
- Is the input ordered with `new[bundle["columns"]]` before predicting?
- Does the file come from a trusted place?
- Do the loaded model's predictions on a few known rows match the
  predictions before saving?
