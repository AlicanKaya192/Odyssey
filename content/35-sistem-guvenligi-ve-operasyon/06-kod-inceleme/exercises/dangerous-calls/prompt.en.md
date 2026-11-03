`dangerous_calls(source)` should find the **calls** to `eval` and `exec`
in Python source and return a list of `"<line>: <name>"`; sorted by line,
left to right within a line. An `eval(` in a comment or a string must not
count: build the tree with `ast.parse` and look at the `ast.Call` nodes
(name `node.func.id`, position `node.lineno` and `node.col_offset`). The
code is not run, only read.

**Expected output:**

```
3: eval
3: eval
4: exec
```
