Two changes:

- When a new run starts on the same branch, the old run still going should be cancelled. The group name is the workflow and the branch: `${{ github.workflow }}-${{ github.ref }}`. At the top level, in the same column as `on`.
- The `test` job should be stopped if it takes longer than 15 minutes.
