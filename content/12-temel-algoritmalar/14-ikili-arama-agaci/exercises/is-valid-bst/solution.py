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
    if node is None:
        return True
    if low is not None and node.value <= low:
        return False
    if high is not None and node.value >= high:
        return False
    return is_bst(node.left, low, node.value) and is_bst(node.right, node.value, high)

def check(spec):
    return is_bst(build_tree(spec))

print(check([5, [3, 1, 6], 8]))
print(check([5, [3, 1, 4], 8]))
print(check(None))
