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
    # An empty spot: a new node. Otherwise go left or right and link.
    return node

def insert_all(values):
    root = None
    for value in values:
        root = insert(root, value)
    return inorder(root)

print(insert_all([8, 3, 10, 1, 6, 14, 4, 7, 13]))
print(insert_all([5, 2, 5, 9, 2]))
