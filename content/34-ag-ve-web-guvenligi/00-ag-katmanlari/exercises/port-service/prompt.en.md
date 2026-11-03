The `WELL_KNOWN` dictionary is ready. `service_for(port)` should
return `"invalid"` if the port is not between 0 and 65535, the service name
if it is in the dictionary, and `"unknown"` otherwise.

**Expected output:**

```
443 https
22 ssh
8081 unknown
70000 invalid
-1 invalid
```
