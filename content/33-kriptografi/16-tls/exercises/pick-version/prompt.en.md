`pick_version(offered)` should accept only the safe versions the client
offers: `"TLSv1.3"` first, otherwise `"TLSv1.2"`; if neither is there,
return the `"protocol_version"` error. The starter code takes the largest
and accepts old versions when only those are offered.

**Expected output:**

```
TLSv1.3
TLSv1.2
protocol_version
```
