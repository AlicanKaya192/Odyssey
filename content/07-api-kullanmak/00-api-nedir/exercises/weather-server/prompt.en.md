Real APIs do not return the answer as plain text but as **status + data**.
The status is a number that says whether the request succeeded: `200` is
success, `404` is not found.

**What to do:**

1. Write the `server(city)` function:
   - if the city is in the `temps` dictionary, return
     `{"status": 200, "temp": <temperature>}`,
   - otherwise return `{"status": 404, "error": "unknown city"}`.
2. The client part: call `server` for every city in the `cities` list.
   If the status is `200`, print `Istanbul: 18`; otherwise print
   `Paris: error 404 (unknown city)`.

**Expected output:**

```
Istanbul: 18
Paris: error 404 (unknown city)
Izmir: 22
```

The client checks the **status** before looking inside the response. That is
the first job when working with real APIs too: did the request succeed?
