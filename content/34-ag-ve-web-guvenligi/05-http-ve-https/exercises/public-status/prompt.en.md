`public_status(found, allowed, logged_in)` should return the status
code for a resource request. If not logged in, `401`. If logged in and
the resource does not exist **or** the person has no permission, `404`:
the existence of someone else's resource is not revealed. If both are
fine, `200`.

**Expected output:**

```
401
200
404
404
```
