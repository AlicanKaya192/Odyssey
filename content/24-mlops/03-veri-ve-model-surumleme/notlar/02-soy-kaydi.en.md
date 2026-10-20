Lineage is the chain that runs from a model back to everything that
produced it:

<figure class="fig">
  <div class="flow">
    <span class="node acc">Model</span>
    <span class="arrow">→</span>
    <span class="node">Training data</span>
    <span class="arrow">→</span>
    <span class="node">Raw data</span>
  </div>
  <figcaption>Every arrow means "produced from". Every link of the chain is known by a hash.</figcaption>
</figure>

## What is in a lineage record?

| Field | Example | Why |
|---|---|---|
| The model's hash | `"model": "dd0ba2458f51"` | Which model file |
| The data's hash | `"data": "fd8e64e44454"` | Which data it was trained on |
| Settings | `{"n_estimators": 50, "random_state": 0}` | How it was trained |
| Library version | `"scikit-learn": "1.9.1"` | In which environment |
| Code version | The Git commit ID | Which training code |
| Parent data | The hash of the older version the data came from | The data's own lineage |

## Questions and where the answer is

| Question | Answer |
|---|---|
| Which data was this model trained on? | The data hash in the lineage record → `get` from the store |
| What changed in the data? | The diff of the two versions by the identifier column |
| Is there another model trained on this data? | Search the lineage records for the same data hash |
| Can I reproduce the same model? | Same data + settings + environment; the model hash should match, or the predictions should |

## Checklist

- Are the data and model files in `.gitignore` and the pointer files in
  Git?
- Is the store kept somewhere else too? A store on a single disk takes
  every version with it when the disk fails.
- Is the hash of a file that is brought back checked?
- Does every model have a lineage record?

## Don't

- Don't let a data file be changed in place and left under the same
  name; new contents mean a new version.
- Don't delete files from the store; one day the data of an old model
  will be needed.
- Don't open a `pickle` file that comes from a source you don't know.
