Write the function `port_from_env(default=8000)`: read the `APP_PORT`
environment variable and return it as an **integer**. If the variable is
missing or is not made of digits only (`str.isdigit`), return `default`. The
starter code crashes when the variable is missing.

**Expected output:**

```
8000
9090 int
8000
```
