Write the function `setup()`: the `"app"` logger's level is `DEBUG`; add
two handlers: to the screen (`sys.stdout`) only `WARNING` and above, in the
format `"%(levelname)s: %(message)s"`; to the file `app.log` (`utf-8`)
everything, in the format `"%(levelname)s %(message)s"`.

**Expected output:**

```
WARNING: config missing
DEBUG reading config
WARNING config missing
```
