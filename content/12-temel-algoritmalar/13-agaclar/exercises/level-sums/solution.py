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


from collections import deque


def level_sums(root):
    if root is None:
        return []
    sums = []
    queue = deque([root])
    while queue:
        total = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            total += node.value
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        sums.append(total)
    return sums

def sums_of(spec):
    return level_sums(build_tree(spec))

print(sums_of(TREE))
print(sums_of(None))
