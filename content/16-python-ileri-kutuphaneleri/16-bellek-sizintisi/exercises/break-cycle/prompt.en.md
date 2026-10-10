The parent points to its child (`children`) and the child to its parent
(`parent`): a cycle. With the garbage collector off (`gc.disable()`), deleting
the root deletes neither. Store `parent` as `weakref.ref(parent)` and make
`parent_node()` return `self.parent()` (`None` if there is no parent). The
expected output:

```
root
['child', 'root']
```

**Expected output:**

```
root
['child', 'root']
```
