| Term | Meaning |
|---|---|
| **Integration** | Adding everyone's changes to the shared code; merging. |
| **Continuous integration** (CI) | Merging small changes often; on every merge the code is installed and tested automatically on a clean machine. |
| **Continuous delivery** | Every change that passes the tests becomes a package ready to release; a person starts the release. |
| **Continuous deployment** | Every change that passes the tests reaches the users automatically. |
| **Pipeline** | The ordered list of stages in the code's journey: install, check, test, package, release. |
| **Stage** | One step of the pipeline; if it fails, the pipeline stops there. |
| **Fail fast** | Catching a problem early and cheaply; fast stages go first. |
| **Green / red build** | A run in which the pipeline passed / failed. |
| **CI service** | The service that runs the pipeline; in this path, GitHub Actions. |
| **Workflow** | The YAML file that describes the pipeline, in `.github/workflows/`. |
| **Trigger** | The event that starts the workflow, for example `push`. |
| **Job** | A group of steps that run on the same machine. |
| **Step** | A single command (`run:`) or a ready-made action (`uses:`). |
| **Action** | A ready-made step written by someone else, like `actions/checkout@v4`; after the `@` comes its version. |
| **Runner** | The clean machine, started from scratch every time, that runs a job. |

The skeleton of a workflow answers three questions:

- **When?** `on:`
- **Where?** `jobs:` → `runs-on:`
- **What?** `steps:`
