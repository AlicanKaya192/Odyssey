`pick_suite(client_suites, server_suites)` should make the server's
choice: return the first suite from the server's list, **in the server's
own preference order**, that the client also supports; if there is no
common suite, `"handshake_failure"`. The starter code always takes the
client's first suite; the server may not support it.

**Expected output:**

```
TLS_AES_128_GCM_SHA256
handshake_failure
```
