def tree_predict(tree, X):
    out = []
    for x in X:
        node = tree
        # Yapraga kadar in.
        out.append(None)
    return out

tree = {"feature": 0, "threshold": 5.0,
        "left": {"leaf": 0},
        "right": {"feature": 1, "threshold": 2.0,
                  "left": {"leaf": 1}, "right": {"leaf": 0}}}
print(tree_predict(tree, [[3, 9], [6, 1], [7, 3]]))
