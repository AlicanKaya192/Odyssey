# Write the imports: pandas, ColumnTransformer, SimpleImputer, Pipeline,
# OneHotEncoder, StandardScaler, LinearRegression, DecisionTreeRegressor,
# RandomForestRegressor, KFold, cross_val_score, train_test_split,
# mean_absolute_error, root_mean_squared_error, r2_score.
# Read the data, take X and y, split (regression has no stratify).


# Build the preprocessor: median + scaling for the numeric columns,
# OneHotEncoder(handle_unknown="ignore") for the text ones.


# The baseline: the training mean for everything. MAE, RMSE and R2.


# Take three models in turn: linear, tree, forest.
# Print one line each: name, CV MAE, CV spread, test MAE, test R2.
# scoring="neg_mean_absolute_error" returns negatives.


# The CV winner and the test winner (the lowest MAE wins).
