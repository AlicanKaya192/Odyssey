# Deployment Strategies

In the tenth section we released a package: users download and install
it themselves. With a web application or a model service things are
different: **we** run the code on a server and users are connected to it
right now. Putting the new version there is called **deployment**. In
this section we see how to connect deployment to the pipeline, how we can
choose to protect users while moving to the new version, and how to go
back when something goes wrong.

## Environments: rehearsal first, then the stage

Code does not go straight to real users. There is at least one
**environment** in between:

<figure class="fig flow">
  <span class="node">Test</span>
  <span class="arrow">→</span>
  <span class="node">staging</span>
  <span class="arrow">→</span>
  <span class="node acc">production</span>
</figure>

- **staging**: an environment as close to the real one as possible, but
  without users. The new version goes here first and is tried here.
- **production**: the environment real users use.

On GitHub each environment is defined on the repository's
**Settings › Environments** page and carries its own rules:

- **Required reviewers**: the job waits until someone on the list says
  "approve". A person starts the move to production.
- **Environment secrets**: production's database password is visible
  only to jobs tied to the `production` environment.
- **Which branches**: for example, production can only be deployed from
  `main` or from `v*` tags.

In a workflow a job is tied to an environment with `environment:`:

```yaml
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py staging
```

## Four ways to move to the new version

The old version is running on the server, users are connected. How do
you move to the new version?

| Strategy | How | Downtime | Going back |
|---|---|---|---|
| Recreate | Stop the old one, start the new one | Yes | Install the old one again |
| Rolling | Replace the servers a few at a time | No, but capacity drops | Roll back gradually |
| Blue-green | Prepare the new one in a separate copy, switch traffic at once | No | Switch traffic back (instantly) |
| Canary | Give a small share of traffic to the new one, measure, then raise it | No | Turn off the canary |

Let's see a rolling deployment with a small model. There are five
servers, two are replaced at each step; a server being replaced does not
serve during that step:

```python
servers = ["web1", "web2", "web3", "web4", "web5"]
batch = 2
updated = []
for start in range(0, len(servers), batch):
    group = servers[start:start + batch]
    serving = len(servers) - len(group)
    print(f"updating {', '.join(group):<11} serving {serving}/5")
    updated += group
    old = len(servers) - len(updated)
    print(f"  after: new {len(updated)}, old {old}")
```

```text
updating web1, web2  serving 3/5
  after: new 2, old 3
updating web3, web4  serving 3/5
  after: new 4, old 1
updating web5        serving 4/5
  after: new 5, old 0
```

Two things show: during the update capacity drops from 5 to 3, and for a
while **two versions run at the same time**. So the new version must be
able to run next to the old one; it must not change the database in a
way the old version cannot understand.

## Canary: a small group first

Miners used to take a canary into the mine: if there was poisonous gas,
the bird was affected first. In a canary deployment, too, the new version
first gets a small share of the traffic (for example 5%); if its error
rate is clearly higher than the old version's, it is pulled back,
otherwise its share is raised.

The decision rests on numbers, but a decision made with few requests
misleads. In the two cases below the new version's error rate is the
same (2%), but in one only 50 requests were seen:

```python
def error_rate(errors, requests):
    return errors / requests


def decide(old, new, max_increase=0.01, min_requests=500):
    if new[1] < min_requests:
        return "wait"
    if error_rate(*new) > error_rate(*old) + max_increase:
        return "rollback"
    return "promote"


old = (40, 10000)
print(decide(old, (1, 50)))
print(decide(old, (20, 1000)))
print(decide(old, (5, 1000)))
```

```text
wait
rollback
promote
```

- The old version fails 0.4% of the time. 1 error in 50 requests is also
  2%, but no decision is made with so few requests: `wait`.
- 20 errors in 1000 requests (2%), more than 1 point above the old one:
  `rollback`.
- 5 errors in 1000 requests (0.5%), within the limit: `promote`, the share
  is raised.

## After deploying: a health check

The deploy command finishing successfully does not mean the application
works. After deploying, a request is sent to the application's **health
address** (`/health`). A freshly started application may not be ready for
a few seconds; the check is tried a few times, waiting in between. If it
never succeeds, the job fails and the pipeline moves on to a **rollback**
step:

```yaml
      - run: python scripts/deploy.py staging
      - run: python scripts/check_health.py "$APP_URL"
        env:
          APP_URL: ${{ vars.STAGING_URL }}
      - run: python scripts/deploy.py staging --rollback
        if: failure()
```

The `failure()` from the fifth section is at step level here: it runs if
an earlier step failed. Since the application's address is not secret, it
is read with `vars` (ninth section).

## Rolling back

The safest way to roll back is deploying **the same package of the
previous version** again; not reverting the code and building again. That
is why the "build once" rule from the eighth section helps here too: each
version's package is kept with its version number, and rolling back means
deploying the old number again.

The only place that needs care is the database. If the new version made a
change (a migration) that deletes a column, going back to the old version
does not bring it back. The common way is two steps: first **expand** (the
new column arrives, the old code ignores it), and once everything has
settled, **remove the old one** in a later version (expand / contract).
This way you can always go back one version.

## Moving to production

```yaml
name: Deploy

on:
  push:
    branches: [main]
    tags: ["v*"]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py staging
  deploy-production:
    needs: deploy-staging
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py production
```

- Every push to `main` goes to staging; production only on a `v` tag and
  only if staging succeeded.
- If reviewers are set on the `production` environment, the job waits
  until the approval comes.
- `environment` can be a dictionary: `url` appears on the run page as a
  link to the live address.
- `concurrency` prevents two production deployments at the same time. In
  the seventh section `cancel-in-progress: true` cancelled tests; a
  deployment is **not cancelled** (`false`): a deployment cut in half
  leaves the server between two versions. The newcomer waits for the
  previous one to finish.
- The deploy jobs get the code because they use `scripts/deploy.py`; the
  package they deploy is still the same file `build` produced.

## Next

What was deployed here was a Python package. In the twelfth section we
put the package into a **container image**, and build, test and push it
to an image registry in the pipeline.

## Summary

- Code goes to staging first, then to production. GitHub environments
  carry reviewers, environment secrets and branch rules; a job is tied
  with `environment:`.
- Recreate causes downtime; in a rolling deployment capacity drops and
  two versions run side by side; blue-green switches traffic at once; a
  canary measures with a small share first.
- A canary decision is made with enough requests; with few requests, you
  wait.
- A health check after deploying; if it fails, roll back with
  `if: failure()`.
- Rolling back is deploying the same package of the previous version
  again. Database changes: expand first, remove later.
- In a production deployment, `concurrency` and
  `cancel-in-progress: false`.
