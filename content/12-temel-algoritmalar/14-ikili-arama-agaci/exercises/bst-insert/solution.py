class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.value] + inorder(node.right)


def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node

def insert_all(values):
    root = None
    for value in values:
        root = insert(root, value)
    return inorder(root)

print(insert_all([8, 3, 10, 1, 6, 14, 4, 7, 13]))
print(insert_all([5, 2, 5, 9, 2]))
