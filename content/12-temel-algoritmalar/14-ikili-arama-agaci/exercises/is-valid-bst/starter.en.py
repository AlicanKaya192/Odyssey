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


def is_bst(node, low=None, high=None):
    # The empty tree is valid. Is the node in range? Then the two subtrees, with new bounds.
    pass

def check(spec):
    return is_bst(build_tree(spec))

print(check([5, [3, 1, 6], 8]))
print(check([5, [3, 1, 4], 8]))
print(check(None))
