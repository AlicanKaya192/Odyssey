What moves the result, and how to pin it down:

| Source | What it does | How to pin it |
|---|---|---|
| `train_test_split` | Shuffles the rows before splitting | `random_state=0` |
| `RandomForestClassifier` | Picks random rows and columns for each tree | `random_state=0` |
| `KFold(shuffle=True)` | Shuffles before splitting into folds | `random_state=0` |
| `KMeans` | Picks the starting centres at random | `random_state=0` |
| Python `random` | A shared generator | Your own generator: `rng = random.Random(0)` |
| NumPy | A shared generator | Your own generator: `rng = np.random.default_rng(0)` |
| Data | Its contents can change silently | A fingerprint: the SHA-256 hash of the contents |
| Libraries | The result can change with the version | Pin with `==` in `requirements.txt` |

## Rules

- Give **each random step its own** seed; don't settle for a single
  `random.seed(0)` at the top of the program.
- The seed is chosen **before** training; it is not changed according to
  the result.
- Compare two models **on the same split**; use cross-validation to get
  away from the luck of a single split.
- `json.dumps(..., sort_keys=True)`: the same dictionary should not give
  a different hash just because its keys are in a different order.
- **Test** reproducibility: two trainings with the same settings, the
  same predictions (compare `predict_proba`).

## Terms

- **Reproducible:** giving the same result when run again with the same
  inputs.
- **Pseudo-random:** a sequence of numbers that looks random but is
  computed from a seed.
- **Seed:** the starting number of that sequence.
- **Hash:** a fixed-length text computed from data; when a single value
  changes, all of it changes.
