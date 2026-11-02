`zones` is a dictionary from part name to zone, `flows` are `[source,
target]` lists.

`boundary_crossings(flows, zones)` should return the flows that cross a
trust boundary as `"source->target"` texts, in list order. If the zone of
one end is **unknown** (not in the dictionary), that flow counts as
crossing too: do not trust something whose zone you do not know.

**Expected output:**

```
student->web
web->db
db->backup
```
