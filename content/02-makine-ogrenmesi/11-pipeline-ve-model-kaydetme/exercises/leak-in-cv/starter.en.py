# Write the imports: you also need numpy, SelectKBest, f_classif,
# cross_val_score, StratifiedKFold and LogisticRegression.
# Prepare, split and preprocess the data.


# Generate 200 columns of random noise (default_rng(7)) and append them.
# Print the total column count.


# The WRONG way: select with SelectKBest(f_classif, k=15) on all the
# training data, then run cross_val_score on those 15. Print the mean.


# The RIGHT way: put the selector and the model in a Pipeline and run
# cross_val_score on all 209 columns. Print the mean.


# Print the gap between them.


# How many of the 15 columns picked the wrong way are noise?
