`audit_config(config)` should check a settings dictionary and return
the list of problems found, in this order:

1. `"debug-on"`: if `debug` is `True`.
2. `"short-password"`: if `password_min` is less than 12; also if the
   setting is **missing** (treat it as 0).
3. `"default-admin"`: if `admin_user` is `"admin"`.
4. `"no-tls"`: if `tls` is not `True`; also if the setting is **missing**.

A missing setting is not considered safe: if you cannot be sure, report a
problem.

**Expected output:**

```
debug-on
short-password
default-admin
no-tls
[]
```
