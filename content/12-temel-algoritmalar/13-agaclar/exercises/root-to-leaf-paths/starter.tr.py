class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_tree(spec):
    # [deger, sol, sag] -> TreeNode; duz deger yaprak; None bos.
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
        # prefix: kokten bu dugume kadarki yol
        pass

    walk(root, "")
    return result

def paths_of(spec):
    return paths(build_tree(spec))

for path in paths_of(TREE):
    print(path)
print(paths_of(None))
