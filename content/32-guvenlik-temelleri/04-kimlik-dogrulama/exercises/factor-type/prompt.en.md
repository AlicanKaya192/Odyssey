`factor_type(method)` should return the kind of factor of an
authentication method:

- `"password"`, `"pin"`, `"passphrase"` → `"know"`
- `"sms_code"`, `"app_code"`, `"security_key"`, `"smart_card"` → `"have"`
- `"fingerprint"`, `"face"`, `"voice"` → `"are"`
- anything not recognised → `"unknown"`

The method name may come in capitals or with spaces: first `strip()` and
`lower()`. The starter code crashes on an unknown method.

**Expected output:**

```
'password' know
'App_Code' have
' fingerprint ' are
'carrier_pigeon' unknown
```
