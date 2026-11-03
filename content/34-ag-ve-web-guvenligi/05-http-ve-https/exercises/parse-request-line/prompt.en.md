`parse_request_line(line)` should split the request line on spaces and
return a `[method, path, version]` list. If the line is not exactly
**three** parts, the method is not in `ALLOWED`, or the path does not
start with `/`, it should return `None`: unexpected input is rejected.

**Expected output:**

```
['GET', '/cart', 'HTTP/1.1']
None
None
None
```
