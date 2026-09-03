# Write the imports: you also need StratifiedKFold and cross_val_score.
# Prepare, split and scale the data. Build the StratifiedKFold.


# Cross validate on the TRAINING data only for k = 1, 3, 5, 7, 9, 15, 25.
# Keep (k, mean, spread) for each and print one line.


# Find the k with the highest mean.


# The noise threshold: the best mean minus its own spread.
# Among the k values above it, take the largest.


# Print the test accuracy for both choices: the CV winner, then the robust k.
