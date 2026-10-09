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


def count_leaves(node):
    # Uc durum: bos agac, yaprak, ic dugum.
    pass

def leaves_of(spec):
    return count_leaves(build_tree(spec))

print(leaves_of(TREE))
print(leaves_of([1, [2, [3, None, 4], None], None]))
print(leaves_of(None))
