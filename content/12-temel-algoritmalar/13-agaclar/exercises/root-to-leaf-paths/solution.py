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


def paths(root):
    result = []

    def walk(node, prefix):
        if node is None:
            return
        path = prefix + "->" + str(node.value) if prefix else str(node.value)
        if node.left is None and node.right is None:
            result.append(path)
            return
        walk(node.left, path)
        walk(node.right, path)

    walk(root, "")
    return result

def paths_of(spec):
    return paths(build_tree(spec))

for path in paths_of(TREE):
    print(path)
print(paths_of(None))
