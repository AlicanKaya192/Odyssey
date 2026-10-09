## Two ways

| | Kahn | DFS |
|---|---|---|
| Idea | take what waits for nothing, decrease the counters | finish the dependencies first |
| Structure | a queue (or a heap) + in-degrees | recursion + three states |
| Cycle | the order stays incomplete | an `active` node is reached again |
| Cost | `O(n + m)` | `O(n + m)` |

A topological order is often **not unique**: jobs that do not wait for each
other (`clean` and `validate`) can be in either order. If a particular order
is wanted (alphabetical), use a heap instead of a queue.

## Where?

- Course prerequisites, installation order (package dependencies; `pip`
  resolves them like this too)
- Build systems: first what depends on the changed file
- Spreadsheet calculations: a cell is calculated after the cells it uses
- Data pipelines: Airflow, dbt, Prefect define jobs as a DAG
- The forward pass in neural networks: the computation graph runs in
  topological order, backpropagation in reverse order

## Shortest and longest paths in a DAG

In a DAG, relaxing in one pass in topological order gives the shortest path in
`O(n + m)` even with negative edges (faster than Dijkstra). Taking `max` in
the same pass gives **the longest path**: the critical path. In a general graph
with cycles the longest path is a very hard problem; in a DAG it is easy.

## Common mistakes

- Mixing up the arrow's direction: "`clean` waits for `extract`" is the same
  as "`extract` → `clean`"; adding the edge backwards reverses the order.
- Forgetting a job with no dependencies that no job waits for: the node set is
  built from both the keys and the values.
- Silently swallowing a cycle: the `len(order) < len(nodes)` check is
  essential in Kahn.
