`request` is a request dictionary (`user`, `inside`, `mfa`,
`device_ok`, `resource`), and `grants` a dictionary of the resources each
user may reach. `access(request, grants)` should return `"allow"` if MFA is
done, the device is sound and the resource is granted to that user, and
`"deny"` otherwise. `inside` (whether it comes from inside the network)
must **not** take part in the decision. The starter code decides with the
perimeter model.

**Expected output:**

```
ada hr-db allow
bob hr-db deny
ada wiki deny
eve wiki deny
```
