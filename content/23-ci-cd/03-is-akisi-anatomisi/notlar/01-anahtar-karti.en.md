**Top level**

| Key | What it is for |
|---|---|
| `name` | The name of the workflow |
| `on` | The triggers |
| `env` | Environment variables valid in every job |
| `jobs` | The jobs (each job's key is its own name) |

**Job** (`jobs.<name>`)

| Key | What it is for |
|---|---|
| `runs-on` | The machine (required): `ubuntu-latest`, `windows-latest`, `macos-latest` |
| `name` | The name on the screen |
| `env` | Variables valid in this job's steps |
| `timeout-minutes` | A time limit |
| `needs` | Jobs that must finish first (the fifth section) |
| `if` | A condition (the fifth section) |
| `strategy` | The matrix (the sixth section) |
| `steps` | The steps (required) |

**Step** (an item of the `steps` list)

| Key | What it is for |
|---|---|
| `name` | The name on the screen |
| `uses` | A ready-made action, with its version |
| `with` | The action's settings |
| `run` | A command; <code>run: &#124;</code> for several lines |
| `env` | Variables valid only in this step |
| `working-directory` | The folder the command runs in |

**Reading a variable**

- Inside a `run` command (bash): `$APP_ENV`
- Outside the command, with the expression syntax: `${{ env.APP_ENV }}`
- If the same name exists at several levels, the one closest to the step
  wins: step > job > workflow.
