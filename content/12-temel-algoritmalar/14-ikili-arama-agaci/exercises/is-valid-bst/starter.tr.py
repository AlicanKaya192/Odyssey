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


def is_bst(node, low=None, high=None):
    # Bos agac gecerli. Dugum aralikta mi? Sonra iki alt agac, yeni sinirlarla.
    pass

def check(spec):
    return is_bst(build_tree(spec))

print(check([5, [3, 1, 6], 8]))
print(check([5, [3, 1, 4], 8]))
print(check(None))
