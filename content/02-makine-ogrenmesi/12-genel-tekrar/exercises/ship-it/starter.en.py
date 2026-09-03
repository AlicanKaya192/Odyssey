# Write the imports: joblib, pathlib.Path, GridSearchCV, StratifiedKFold,
# LogisticRegression, average_precision_score.
# Prepare and split the data (no followup_calls, stratify=y).


# Build the pipeline: preprocessor + LogisticRegression(balanced).


# Search with GridSearchCV (scoring="average_precision").
# Print the best C, the best strategy and the CV score on one line.


# Save the best pipeline as model.joblib.
# Is the file larger than 1000 bytes?


# Load it back and print the average precision on the test set.


# Build a DataFrame of three new patients.
# Use None for bmi and region on the second row.


# Print the three patients' probabilities.


# Print the predictions produced with a 0.3 threshold.
