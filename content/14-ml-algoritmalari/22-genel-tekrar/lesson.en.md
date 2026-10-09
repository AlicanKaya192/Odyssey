# Overall Review

You have reached the end of ALG 3. You wrote most machine learning algorithms
**from scratch** with NumPy and compared their results with scikit-learn. Now
when you call a library function you know what runs behind it: which loss it
minimises, which assumption it rests on, where it goes wrong. This section
gathers the essence of each algorithm and the most important results we
measured in one place.

<figure class="fig">
  <div class="flow">
    <span class="node">Foundations<br><small>00–02</small></span><span class="arrow">→</span>
    <span class="node">Linear models<br><small>03–07</small></span><span class="arrow">→</span>
    <span class="node">Classifiers<br><small>08–13</small></span><span class="arrow">→</span>
    <span class="node">Unsupervised<br><small>14–19</small></span><span class="arrow">→</span>
    <span class="node acc">Networks, recs<br><small>20–21</small></span>
  </div>
  <figcaption>The path of ALG 3: learn to measure, build linear models, compare classifiers, move to unlabelled data, and finally neural networks and recommendation.</figcaption>
</figure>

## 1. Foundations (Sections 0–2)

The first lesson of writing algorithms from scratch is **vectorisation**:
array operations like `X @ w` instead of Python loops. The second is the
**baseline**: even a "model" that always says the most frequent class gets
some accuracy; a real model must beat it. In statistics, watch numerical
precision: computing the variance in one pass with the naive formula breaks
on large numbers, Welford's method does not. How good a model is gets measured
by **resampling**: a single split depends on luck, k-fold cross-validation is
more stable; a permutation test answers "is this result luck?".

## 2. Linear models (Sections 3–7)

- **Linear regression:** the normal equation or gradient descent; with highly
  related features the coefficients grow meaninglessly, and a high-degree
  polynomial explodes on test data.
- **Gradient descent:** the learning rate and **scaling** decide; on unscaled
  data the same problem did not finish even in a hundred thousand steps,
  after scaling it finished in 23.
- **Logistic regression:** sigmoid + log loss; softmax for many classes.
- **Evaluation:** the confusion matrix, precision/recall/F1, ROC and AUC.
  Accuracy misleads on imbalanced data.
- **Regularisation:** Ridge (L2) shrinks coefficients, Lasso (L1) sets some
  exactly to zero; the strength is chosen with cross-validation.

## 3. Classifiers (Sections 8–13)

| Algorithm | Idea | Watch out |
|---|---|---|
| KNN | the vote of the `k` nearest neighbours | scaling, the curse of dimensionality |
| Naive Bayes | class probability × feature probabilities | sum logs (underflow), Laplace smoothing |
| Decision tree | the split that purifies most (Gini) | depth limit, overfitting |
| Random forest | the vote of trees, randomness in each tree | free validation with OOB |
| Boosting | each new tree on the previous ones' errors | learning rate, early stopping |
| SVM | the boundary with the largest margin, hinge loss | `C`, kernel, scaling |

The value of going from a tree to a forest was measured: a single tree 0.738,
bagging 0.80, random forest 0.814; the OOB estimate 0.828. For boosting and
SVM our own versions gave the same or very close results to scikit-learn.

## 4. Unlabelled data (Sections 14–19)

- **k-Means:** assign and update; depends on the start, 4 of 100 random
  starts got stuck in a local minimum, k-means++ cut that to 1. `k` by the
  elbow and the silhouette.
- **GMM and EM:** soft assignment, elliptical clusters; the number of
  components by BIC.
- **Hierarchical and DBSCAN:** building and cutting a tree; clusters and
  noise by density. On noisy moons DBSCAN 1.0, k-Means 0.221.
- **PCA:** the eigenvectors of the covariance; on the digit data 90% of the
  variance of 64 pixels is in 21 components. PCA without scaling finds the
  column with the largest unit.
- **Association rules:** support, confidence, lift; Apriori pruning.
  Confidence misleads (tea → milk 0.615 but lift 1.05).
- **PageRank:** the random surfer, power iteration; links are not counted
  but weighed.

## 5. Neural networks and recommendation (Sections 20–21)

A neural network is neurons in layers; backpropagation carries derivatives by
the chain rule and is checked against numerical derivatives. One neuron
cannot solve XOR, three hidden neurons can. Weights must start at random,
otherwise the neurons stay identical. In recommender systems matrix
factorisation finds the hidden tastes: a test error of 0.628, better than all
baselines, and the hit rate of the top 5 recommendations is about 1.8 times
that of popularity.

## Common lessons

1. **Baseline first.** Compare every model with a simple rival.
2. **Scale.** Every method resting on distance or gradients (KNN, SVM,
   k-Means, PCA, gradient descent) is sensitive to scale.
3. **Do not touch the test data.** Scaling, PCA, selection; all fit only on
   training data (`Pipeline`).
4. **Choose settings with cross-validation.** `k`, `C`, `alpha`, depth, the
   number of components.
5. **Complexity is not free.** If training error falls while test error
   rises, the model is memorising.
6. **Verify what you write from scratch.** Compare with the library, with
   numerical derivatives, with brute force.

## In this section

40 mixed questions and five exercises: scaling without leakage, computing
classification measures, predicting with KNN, finding the best tree split and
training logistic regression with gradient descent. The lesson notes hold
quick-reference patterns and what comes next.
