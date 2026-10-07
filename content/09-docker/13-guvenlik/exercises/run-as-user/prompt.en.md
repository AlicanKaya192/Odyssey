This image runs the program as root.

**What to do:**

1. Create the user `app` with `useradd --create-home --uid 1000 app`.
2. The container should run as the `app` user (`USER`).

**Expected output:**

```
running as app
```
