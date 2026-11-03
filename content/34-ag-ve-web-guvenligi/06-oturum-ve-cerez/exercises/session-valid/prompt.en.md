`valid(created, last_seen, now, idle, absolute)` should return `True`
if the session has exceeded neither the idle timeout (`now - last_seen <
idle`) nor the absolute timeout (`now - created < absolute`), and `False`
otherwise. The starter code looks only at idleness.

**Expected output:**

```
True
False
False
```
