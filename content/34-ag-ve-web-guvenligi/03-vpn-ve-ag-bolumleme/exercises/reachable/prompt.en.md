`links` lists the devices each device can reach directly.
`reachable(links, start)` should return all devices that can be reached
from the start, **indirectly** too, excluding the start itself, in
alphabetical order. The starter code finds only the direct neighbours; it
misses lateral movement chains.

**Expected output:**

```
['hr-db', 'web']
['hr-db']
[]
```
