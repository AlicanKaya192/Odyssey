Write the function `get_logger(name)`: return a logger with a `"shop."`
prefixed name (`logging.getLogger(f"shop.{name}")`). Two calls with the same
name must give the same object.

**Expected output:**

```
shop.db True 30
```
