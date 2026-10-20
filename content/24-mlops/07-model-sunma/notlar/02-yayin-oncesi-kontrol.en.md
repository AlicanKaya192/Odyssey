Before releasing a service that serves a model:

## Checklist

- Is the model file the same as the registered version (does the hash
  match)?
- Are the library versions in `requirements.txt` the same as in training
  and pinned with `==`?
- Is the model loaded at startup? Doesn't the first request make it load?
- Does input validation use the same rules as the training schema?
- Does the feature code come from **the same file** as in training?
- Does `/health` say the model version?
- Is the model version in the answers and in the batch result files?
- Was the speed promise made in terms of p95, and was it measured?
- Does the image run as a non-root user?
- Is the way back clear? (The previous image tag, or the previous version
  in the registry.)

## Two ways to package

| | Model inside the image | Model from the registry at startup |
|---|---|---|
| Image tag | Carries the model version (`churn-api:3`) | Carries the code |
| When the model changes | A new image is built | The alias changes, the image stays |
| Startup | No outside dependency | Depends on the registry and the network |
| Rolling back | Go back to the old image | Point the alias at the old version |

## Don't

- Don't load the model per request.
- Don't write the feature code twice for training and serving; two
  copies drift apart sooner or later.
- Don't report speed with the average.
- Don't record predictions without the model version; later nobody knows
  which model decided.
