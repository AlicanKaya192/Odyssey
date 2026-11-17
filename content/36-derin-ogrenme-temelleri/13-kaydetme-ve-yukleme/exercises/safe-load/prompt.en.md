`load_kind(path)` loads the file in the unsafe mode. Switch it to the safe mode:
load with `weights_only=True`; if the file is refused
(`pickle.UnpicklingError`) return `"refused"`, if it loads return `"ok"`. The
program should print `ok refused`.

**Expected output:**

```
ok refused
```
