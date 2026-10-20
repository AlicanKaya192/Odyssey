Before you release a model that measures well in a notebook, you should
be able to answer these questions. Each one is the subject of a section
in this module.

## Reproduce

- If I train the model again with the same data and the same code, do I
  get the same result? (Reproducible Training)
- Which data, which code and which settings were used, and where is that
  written down? (Data and Model Versioning, Experiment Tracking)

## Trust

- Is the data going into training in the expected shape: columns, types,
  ranges, missing values? (Data Validation)
- Is the new model really better than the old one, and were they
  compared on the same measure? (The Model Registry, CI for ML)

## Serve

- How is the model packaged, and how does whoever needs a prediction
  reach it? (Packaging and Serving a Model)
- Is the data prepared the same way in training and in serving?
  (Training-Serving Skew)

## Monitor

- How will I know the model is getting worse? Which number am I watching?
  (Monitoring)
- Did the incoming data change, or did the relationship between the data
  and the outcome? (Data Drift, Concept Drift)
- How do I try a new model before opening it to everyone? (A/B Tests,
  Shadow and Canary)

## Don't

- Don't measure the model only once, right after training, and leave it.
- Don't say "it raises no error, so it works": a model can predict
  wrong without raising an error.
- Don't share a model file without writing down where it came from.
