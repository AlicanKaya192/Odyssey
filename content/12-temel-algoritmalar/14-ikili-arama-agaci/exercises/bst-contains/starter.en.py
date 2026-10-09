class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node


def build_bst(values):
    root = None
    for value in values:
        root = insert(root, value)
    return root


VALUES = [8, 3, 10, 1, 6, 14, 4, 7, 13]


def contains(node, target):
    # Go down until the node is None.
    pass

def contains_in(values, target):
    return contains(build_bst(values), target)

print(contains_in(VALUES, 6), contains_in(VALUES, 5))
print(contains_in([], 1))
