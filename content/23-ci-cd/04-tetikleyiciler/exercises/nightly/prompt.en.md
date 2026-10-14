The tests run on pushes to `main`. Add two triggers:

- It should run every day at **06:00 Turkey time** (`schedule`, minute `0`).
- It should be possible to start it by hand from the Actions tab.

The hour in the cron is UTC.
