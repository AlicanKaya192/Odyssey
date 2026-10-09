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


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)


def minimum(node):
    while node.left:
        node = node.left
    return node.value


def delete(node, value):
    if node is None:
        return None
    # First find the value (go left/right), then the three cases.
    return node

def after(values, removed):
    root = build_bst(values)
    for value in removed:
        root = delete(root, value)
    return [inorder(root), root.value if root else None]

print(after([8, 3, 10, 1, 6, 14, 4, 7, 13], [7, 14, 3]))
print(after([8, 3, 10, 1, 6, 14], [8]))
print(after([5], [5]))
