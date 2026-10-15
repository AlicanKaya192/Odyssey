**Permissions: least privilege**

```yaml
permissions:
  contents: read

jobs:
  release:
    permissions:
      contents: write
```

- The block at the top is the default for all jobs; a block in a job
  overrides it.
- Once `permissions:` is written, every permission not in the list
  becomes `none`.

| Permission | For | Most jobs |
|---|---|---|
| `contents` | Files, tags, releases | `read`; the job that creates a release `write` |
| `pull-requests` | Comment, label on a PR | `write` if needed |
| `packages` | Package and image registry | The job that uploads `write` |
| `id-token` | Logging in to a cloud without a password | The job that deploys `write` |

**Pinning actions**

| Form | Can it change? |
|---|---|
| `actions/checkout@v4` | Yes; the tag can be moved to another commit |
| `actions/checkout@main` | Every day; the branch moves on |
| `actions/checkout@` + 40-character commit id | No |

When pinning by a commit id, write the version as a comment at the end of
the line (`# v4`); update it by hand or with Dependabot.

**Code injection**

Values from outside: the PR title and body, the branch name, the commit
message, a comment's text, an issue title. These are not written straight
into `run:`.

```yaml
      # Dangerous: the title becomes part of the command
      - run: echo "PR title is ${{ github.event.pull_request.title }}"
```

```yaml
      # Safe: the title becomes a variable's value
      - run: echo "PR title is $TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

**Careful with `pull_request_target`**

`pull_request` gives no secrets to a PR from a fork. `pull_request_target`
instead runs the workflow with the target branch's version, with secrets
and write permission. Getting and running the PR's code under this
trigger means handing the secrets to whoever opened the PR. Do not use it
unless you must.

**Checklist**

- No key in the code; all of them in the store.
- A secret is given with `env:` only to the step that needs it.
- `permissions: contents: read` at the top.
- Jobs that need secrets do not run in a PR.
- Text from outside goes through `env:`.
- Trusted actions; pinned by a commit id in a critical pipeline.
