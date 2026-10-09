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


def tree_sum(node):
    # Taban durumu: bos agac.
    # Sonra: kendi degerin + iki alt agacin toplami.
    pass

def sum_of(spec):
    return tree_sum(build_tree(spec))

print(sum_of(TREE))
print(sum_of(None))
