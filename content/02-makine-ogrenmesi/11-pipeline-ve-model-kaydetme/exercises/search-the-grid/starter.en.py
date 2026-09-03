# Write the imports: you also need GridSearchCV, StratifiedKFold,
# LogisticRegression and accuracy_score.
# Prepare, split the data and build the pipeline.


# Set up the StratifiedKFold.


# Define the two-parameter grid:
#   prepare__num__impute__strategy: ["median", "mean"]
#   model__C: [0.01, 0.1, 1, 10]


# Search with GridSearchCV. Print one line per point:
# the strategy, C, the CV mean.


# Print the best settings and that setting's CV score.


# The search's test accuracy and the untuned pipeline's, side by side.
