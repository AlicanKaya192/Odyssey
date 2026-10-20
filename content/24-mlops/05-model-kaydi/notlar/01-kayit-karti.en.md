The parts of a model registry:

| Part | Example | What it is for |
|---|---|---|
| Model name | `churn` | The family of models that do the same job |
| Version | `3` | Never changes, never reused |
| File and its hash | `models/churn-v3.pkl`, `sha256` | Which file; noticed if it changes |
| Measurements | `{"accuracy": 0.818}` | Comparison at the gate |
| Note | `"more data"` | What changed in this version |
| Alias | `production -> 3` | The version in production |
| History | `[["production", 1], ["production", 3]]` | The versions the alias pointed at, in order |

## The life cycle

<figure class="fig">
  <div class="flow">
    <span class="node">Train</span>
    <span class="arrow">→</span>
    <span class="node">Register</span>
    <span class="arrow">→</span>
    <span class="node acc">Gate</span>
    <span class="arrow">→</span>
    <span class="node ok">Production</span>
  </div>
  <figcaption>A version that doesn't pass the gate stays in the registry but gets no alias.</figcaption>
</figure>

## The gate rule

- The candidate and the version in production are measured on the
  **same** evaluation set.
- The alias moves to the candidate only if it beats the one in
  production by at least a threshold (`min_gain`).
- If no version is in production yet, the first version goes straight
  into production.

## Rolling back

- Point the alias at the old version: `set_alias("churn", "production", 1)`.
- No new training is needed; the old file is in the registry.
- The condition: the old versions' files are not deleted.

## Terms

- **Model registry:** the place that keeps models' versions, files,
  measurements and aliases.
- **Alias:** a name attached to a version, such as `production` or
  `staging`.
- **Promotion:** a version getting an alias, for example going into
  production.
- **Rollback:** pointing the alias back at an earlier version.
