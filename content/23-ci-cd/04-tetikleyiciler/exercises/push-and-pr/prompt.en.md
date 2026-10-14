This workflow runs on every push to every branch. Change it so that:

- It runs on pushes to the `main` branch (`push` + `branches`).
- It runs on pull requests opened against `main` (`pull_request` + `branches`).

Turn the `on: push` line into the form where settings are written under the events.
