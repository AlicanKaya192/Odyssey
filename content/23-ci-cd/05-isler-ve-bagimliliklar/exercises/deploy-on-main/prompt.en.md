Add a `deploy` job at the end of the file:

- It should start when `build` finishes.
- It should run only on **pushes to the `main` branch**, not on pull requests. The condition has both the event (`github.event_name`) and the branch (`github.ref`).
- The machine is `ubuntu-latest`; the steps: get the code, then run `./deploy.sh`.
