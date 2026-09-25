You have finished MATH 2. The mathematical foundation of AI is now in your hands; there are several ways on from here.

## The Machine Learning path

The code counterparts of the formulas you derived here are in the Machine
Learning path:

| In MATH 2 | In code |
|---|---|
| normal equations, least squares | training linear regression |
| sigmoid, log-loss, gradient | logistic regression |
| entropy, information gain | impurity in decision trees |
| standard error, sampling | the spread of validation scores |
| covariance, PCA | unsupervised learning and dimensionality reduction |
| distance, norm | KNN and clustering |

## Write it yourself

The best way to make the mathematics stick is to code it from scratch.
With nothing but NumPy:

- solve linear regression first with the normal equations, then with
  gradient descent, and compare the two results;
- train logistic regression with the $(p - y)x$ gradient and watch the
  log-loss fall;
- compute PCA separately with the eigenvectors of the covariance matrix
  and with the SVD.

## Suggestions for review

- If you got stuck in a section, go back first to its **reference note**,
  then to its **worked examples**.
- Every question you miss in the review quiz points to a section; the
  tables in the Quick Reference show which one to go to.
- For the calculus branch, Derivative Rules and Gradient Descent, and for
  the probability branch, Conditional Probability and Bayes and Sampling,
  are the most used foundations.
