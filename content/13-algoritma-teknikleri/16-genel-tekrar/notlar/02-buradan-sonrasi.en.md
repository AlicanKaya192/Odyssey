## Where will these techniques show up?

- **In machine learning:** a decision tree choosing the best split is greedy;
  gradient descent is a local search; k-means lands in a local optimum; DTW and
  sequence alignment are dynamic programming; recommender systems find similar
  users with MinHash and LSH.
- **In data engineering:** pipelines are DAGs and run in topological order; in
  large tables the number of distinct values is estimated with HyperLogLog and
  frequent values with Count-Min; duplicate records are grouped with
  union-find.
- **In interviews:** most medium and hard questions are the patterns of these
  sections: the "graph", "dynamic programming", "backtracking", "greedy",
  "union find", "monotonic stack", "binary search" tags.

## How to practise?

1. Before writing code, estimate the budget: how large can `n` be, which
   complexity fits?
2. Write brute force first; test the fast solution against it with random
   inputs.
3. When stuck, go back to the "Which technique for which question?" table.
4. In DP, first define the state in one sentence; the table comes after.
5. A week later, solve the same problem again without looking at your notes.

## What comes next?

**Data Science and Machine Learning Algorithms**

Linear and logistic regression, gradient descent, decision trees, random
forests and gradient boosting, k-nearest neighbours, k-means and DBSCAN, PCA,
Naive Bayes, SVM, EM, Apriori, PageRank, neural networks and recommender
systems: all written from scratch with NumPy and compared with scikit-learn.
