Add a `notify` job at the end of the pipeline:

- It should wait for `deploy`.
- It should run only when something in the pipeline **fails**.
- The machine is `ubuntu-latest`; one step: print a message with `echo`.

Careful: if a test fails, `deploy` does not fail, it is **skipped**. The condition must cover this too.
