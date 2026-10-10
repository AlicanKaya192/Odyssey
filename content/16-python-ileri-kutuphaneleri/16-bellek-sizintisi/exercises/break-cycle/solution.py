import gc
import weakref


class TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.parent = weakref.ref(parent) if parent is not None else None

    def parent_node(self):
        return self.parent() if self.parent is not None else None


gc.disable()
freed = []
root = TreeNode("root")
child = TreeNode("child", parent=root)
root.children.append(child)
weakref.finalize(root, freed.append, "root")
weakref.finalize(child, freed.append, "child")
print(child.parent_node().name)
del root, child
print(sorted(freed))
gc.enable()
