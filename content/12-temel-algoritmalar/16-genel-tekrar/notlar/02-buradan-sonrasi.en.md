## Where will what you learned here help?

- **When working with data:** the ideas from these sections run behind pandas
  and SQL. `merge` and `JOIN` use a hash table, `CREATE INDEX` a B-tree,
  `sort_values` a sorting algorithm, `rolling` a sliding window, `cumsum`
  prefix sums.
- **In machine learning:** prediction in a decision tree is a walk from the
  root to a leaf, KNN looks for the `k` nearest neighbours (a heap, a k-d
  tree), recommender systems pick the best `k`.
- **In code reviews and interviews:** you now ask "what does that `in` inside
  the loop cost?". Most technical interviews are slightly changed versions of
  the patterns in these sections.

## How to practise?

1. When you read a problem, before writing code, state the **brute-force**
   solution and its cost (like `O(n²)`).
2. Look at the "Which tool for which question?" table: where is the repeated
   work? Does a dictionary, a pointer or a prefix sum remove it?
3. Write the edge cases first: empty input, one element, all the same,
   negatives.
4. After writing it, **measure the time** with a large input; is it the growth
   class you expected?
5. A week later, solve the same problem again without looking.

Coding problem sites (easy and medium level) are very close to the exercises
of these sections; the tags "array", "hash table", "two pointers", "sliding
window", "stack", "tree", "heap" map directly to these sections.

## What comes next?

**Algorithm Techniques and Graphs**

- Divide and conquer, backtracking, greedy algorithms
- Dynamic programming (two sections): solving repeated subproblems once
- Graphs, graph traversal, shortest paths (Dijkstra), topological sorting,
  spanning trees and union-find
- String and number algorithms, randomised algorithms
- Probabilistic data structures (Bloom filters, HyperLogLog), heuristic
  optimisation

**Data Science and Machine Learning Algorithms**

Regression, gradient descent, decision trees, ensemble methods, SVMs,
clustering, PCA, neural networks and recommender systems from scratch with
NumPy.
