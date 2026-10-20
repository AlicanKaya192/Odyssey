Write the function `route(customer_id, percent)` for the lesson's routing:

- `customer_id` is a string (like `"C06-00001"`).
- The bucket: `zlib.crc32(customer_id.encode()) % 100`.
- Return `"new"` if the bucket is less than `percent`, otherwise `"old"`.

**Expected output:**

```
39
old new
True
```
