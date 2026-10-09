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


def kth_smallest(root, k):
    values = []
    # Inorder: left, root, right.

    return None

def kth_of(values, k):
    return kth_smallest(build_bst(values), k)

for k in [1, 3, 9, 10]:
    print(k, kth_of(VALUES, k))
