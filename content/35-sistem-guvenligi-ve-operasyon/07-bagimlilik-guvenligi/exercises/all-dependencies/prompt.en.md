`graph` is package → list of direct dependencies. `all_dependencies(graph,
root)` should return all the direct and transitive dependencies of
`root`, **once each** and in alphabetical order; `root` itself must not be
in the list. The graph may have a cycle: the starter code's recursion runs
forever there.

**Expected output:**

```
db, escape, http, pool, templates, web
http, pool
```
