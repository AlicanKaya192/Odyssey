# Write the imports: pandas, ColumnTransformer, SimpleImputer, Pipeline,
# OneHotEncoder, StandardScaler, LogisticRegression, train_test_split,
# accuracy_score.
# Read the data and print the missing-value counts as a dict.


# Take X and y, then train_test_split.


# Build a ColumnTransformer: median + scaling for the numeric columns,
# most frequent + OneHotEncoder(handle_unknown="ignore") for the text ones.


# Join it into a Pipeline with LogisticRegression(max_iter=1000) and fit.


# Print the baseline and the test accuracy side by side.


# Print the column count and the column names after preprocessing.
