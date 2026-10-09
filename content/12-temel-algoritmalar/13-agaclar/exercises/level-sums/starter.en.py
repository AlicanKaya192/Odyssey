class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_tree(spec):
    # [value, left, right] -> TreeNode; a plain value is a leaf; None is empty.
    if spec is None:
        return None
    if not isinstance(spec, list):
        return TreeNode(spec)
    value, left, right = spec
    return TreeNode(value, build_tree(left), build_tree(right))


TREE = [1, [2, 4, 5], [3, None, 6]]


from collections import deque


def level_sums(root):
    if root is None:
        return []
    sums = []
    queue = deque([root])
    # Handle one level per round.

    return sums

def sums_of(spec):
    return level_sums(build_tree(spec))

print(sums_of(TREE))
print(sums_of(None))
