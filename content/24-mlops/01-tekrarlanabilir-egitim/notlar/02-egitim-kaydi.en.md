To reproduce a training run six months later, its record should hold:

| Field | Example | Why |
|---|---|---|
| Configuration | `{"rows": 2000, "split_seed": 0, ...}` | All settings and seeds |
| Data fingerprint | `"a91a352912da"` | Exactly which data |
| Code version | Git commit ID | Which training code |
| Environment | Python and library versions | The same calculation methods |
| Result | `"accuracy": 0.768` | To compare when reproducing |
| Date | `"2026-10-20"` | When |

The code version was not written in this section, because the exercises
do not run in a Git repository. In a real project the commit ID given by
`git rev-parse HEAD` is added to the record (the Git path).

## An example record

```text
{
  "config": {"rows": 2000, "data_seed": 7, "split_seed": 0,
             "n_estimators": 50, "model_seed": 0},
  "data": "a91a352912da",
  "python": "3.14.7",
  "scikit-learn": "1.9.1",
  "accuracy": 0.768
}
```

## Checklist

- Is training in one function that looks only at the configuration?
- Does every random step have its own seed?
- Are the library versions pinned with `==`?
- Is the record kept next to the model?
- Is there a test that checks two trainings with the same configuration
  give the same predictions?

## Don't

- Don't try seeds and pick the one with the best result.
- Don't change a setting inside the code without recording it: every
  setting that changes should go through the configuration.
- Don't identify data by its file name; the contents may have changed.
