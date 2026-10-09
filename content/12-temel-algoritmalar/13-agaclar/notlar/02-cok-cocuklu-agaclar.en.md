Folders, JSON documents, the submenus of a menu: most real-life trees are not
binary; a node has **as many** children as it likes. The only difference is
keeping a **list of children** instead of `left` and `right`. The skeleton is
the same: a base case and combining the children's answers.

```python
folders = {"name": "project", "size": 2, "children": [
    {"name": "data", "size": 120, "children": [
        {"name": "raw", "size": 300, "children": []}]},
    {"name": "src", "size": 15, "children": []},
]}

def total_size(folder):                       # postorder: children first
    return folder["size"] + sum(total_size(c) for c in folder["children"])

def show(folder, depth=0):                    # preorder: itself first
    print("    " * depth + folder["name"], total_size(folder))
    for child in folder["children"]:
        show(child, depth + 1)

show(folders)
```

```text
project 437
    data 420
        raw 300
    src 15
```

Here, if the list of children is empty the loop never runs; no separate `if`
is needed. The base case is a node with no children.

One caution: `show` calls `total_size` again at every node, so subtrees are
walked over and over. If the tree is large, it is better to compute the sizes
once and keep them (or do both in a single postorder pass).

## The depth of a nested list

A nested Python list is a tree too: each list is a node, the lists inside it
are its children.

```python
def depth(item):
    if not isinstance(item, list):
        return 0
    return 1 + max((depth(x) for x in item), default=0)

print(depth([1, [2, [3, 4]], [5]]), depth([]), depth(7))
```

```text
3 1 0
```

`max`'s `default=0` is for the empty list: an empty list has depth 1.
