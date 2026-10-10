This module showed a model's whole path on tabular data with the libraries.
From here the road opens in a few directions.

## In this program

| Track / module | Which part of this module |
|---|---|
| Machine Learning | the concepts themselves: validation, overfitting, imbalanced data |
| ML Algorithms | writing the models used here from scratch with NumPy |
| Time Series | `TimeSeriesSplit`, statsmodels; validation in time |
| Writing REST APIs with FastAPI | putting a saved model behind an API |
| Docker | packaging the model and its environment with pinned versions |
| Big Data | preparing features on data that does not fit in memory |

## Outside the program

- **Deep learning:** neural networks for unstructured data like images,
  sound and text (PyTorch, TensorFlow). On tabular data boosting is often
  better or equal; on unstructured data neural networks lead.
- **Other boosting libraries:** XGBoost and CatBoost are from the same family
  as LightGBM; their scikit-learn interfaces are nearly the same.
- **Model explanation:** libraries like SHAP break a single prediction down
  into the columns it came from; a continuation of permutation importance and
  ICE.
- **Model monitoring:** a model in production decays over time (the data
  changes); the distributions of predictions and inputs are watched and the
  model is retrained when needed.

## On your own

- scikit-learn's "User Guide" explains with examples when each class is
  useful; it contains many tools not covered in this module.
- Walk this module's path with your own data from start to finish: split,
  prepare, validate, search, choose a threshold, test, explain, save. The ten
  steps in the Quick Reference note are the list of that path.
