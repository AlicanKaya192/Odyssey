# CI/CD with Containers

In the eleventh section the thing we deployed was a Python package: the
server needed the right Python version and the right libraries
installed. A **container** removes this problem: the application is put
into a single **image** together with everything it needs to run, and
that image runs the same on every machine. In this section we set up
the pipeline to build the image, run the tests inside the image and send
the image to an **image registry**.

## A short reminder: image, container, registry

If you have not read the Docker path, four words are enough:

<figure class="fig anat">
  <div class="anat-row"><span>Dockerfile</span><span>The image's recipe: which base to start from, which files to copy, which command to run.</span></div>
  <div class="anat-row"><span>Image</span><span>The unchanging package built from the recipe. Application + Python + libraries.</span></div>
  <div class="anat-row"><span>Container</span><span>A running copy of an image.</span></div>
  <div class="anat-row"><span>Image registry</span><span>Where images are stored and downloaded from. GitHub's is <code>ghcr.io</code>.</span></div>
</figure>

For the pipeline this means: the package in the "build once" rule from
the eighth section is now an image. The pipeline builds the image once,
tests **that image**, sends **that image** to the registry; the server
runs the same image too.

<figure class="fig">
  <div class="flow">
    <span class="node">build</span>
    <span class="arrow">→</span>
    <span class="node">test in image</span>
    <span class="arrow">→</span>
    <span class="node">push</span>
    <span class="arrow">→</span>
    <span class="node acc">deploy</span>
  </div>
</figure>

## Building the image and testing inside it

GitHub's `ubuntu-latest` machine comes with Docker installed. Docker's
own actions are used to build an image:

```yaml
  image:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: greeter:test
      - run: docker run --rm greeter:test python -m pytest -q
```

- `setup-buildx-action` prepares the builder (Buildx); features like
  caching come with it.
- `build-push-action` builds the image from the `Dockerfile`.
  `context: .` says the build looks at the root of the repository.
- `load: true` loads the built image into the machine's own Docker;
  otherwise the image stays inside the builder and `docker run` cannot
  find it.
- The last step runs the tests **inside the image**. If the tests pass,
  what we know is no longer "the code works" but "this image works".

For the tests to run inside the image, the test files and `pytest` must
be in the image. Teams that do not want this set up a separate test
stage (multi-stage); the basic idea is the same: the image that is tried
and the image that is sent come from the same recipe.

## Naming the image: tags

In an image registry the same image can have many names (tags). Which
tag is given when is a rule. A common rule:

- On every build the **commit id** (SHA): every image is unique and
  traceable.
- On a push to `main`, `latest`: "the newest state".
- On a `v1.4.2` tag, the version number and its short form `1.4`.

```python
def image_tags(image, ref, sha):
    tags = [f"{image}:{sha[:7]}"]
    if ref == "refs/heads/main":
        tags.append(f"{image}:latest")
    if ref.startswith("refs/tags/v"):
        version = ref.removeprefix("refs/tags/v")
        major, minor, _ = version.split(".")
        tags.append(f"{image}:{version}")
        tags.append(f"{image}:{major}.{minor}")
    return tags


image = "ghcr.io/ada/greeter"
sha = "4f2a9c81d0e5b7a3c6e1f09d8b2a4c7e5f3d1b09"
for ref in ["refs/heads/main", "refs/heads/login", "refs/tags/v1.4.2"]:
    print(ref)
    for tag in image_tags(image, ref, sha):
        print("  " + tag)
```

```text
refs/heads/main
  ghcr.io/ada/greeter:4f2a9c8
  ghcr.io/ada/greeter:latest
refs/heads/login
  ghcr.io/ada/greeter:4f2a9c8
refs/tags/v1.4.2
  ghcr.io/ada/greeter:4f2a9c8
  ghcr.io/ada/greeter:1.4.2
  ghcr.io/ada/greeter:1.4
```

The branch build (`login`) gets only the SHA tag; writing `latest` on
top of a feature branch would turn "the newest state" into the wrong
image.

**Deploying with `latest`.** `latest` points to another image on every
push to `main`. If the server runs `latest`, when you want to go back two
weeks later there is no name called "the previous one". Deployment uses
a tag that does not change (the SHA or the version); the rollback from
the eleventh section is only possible this way.

## Sending the image to the registry

The image will be sent to `ghcr.io`. No separate password is needed to
log in: the `GITHUB_TOKEN` from the ninth section is enough, as long as
the job asks for the `packages: write` permission.

```yaml
  publish:
    needs: image
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/ada/greeter:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

- `if: github.event_name == 'push'`: in a PR the image is built and
  tested but **not sent**. We do not want a PR from a fork to put an
  image into the registry; secrets come empty there anyway.
- `docker/login-action` logs into the registry; instead of a password,
  the run's temporary key.
- `push: true` sends the image to the registry.
- The image name in the registry must be **lowercase**. If the user or
  repository name has capital letters, write the name in lowercase by
  hand.

## The layer cache

An image is made of layers: every step in the Dockerfile is one layer.
Docker does not run a step again if that step and everything before it
did not change; it uses the layer from the cache. When a step changes,
**that step and every step after it** run again.

On your own computer this cache is always there. The pipeline's machine,
however, starts **from scratch** on every run: without a cache every
build runs every step from the beginning. Let's see this with a small
model (a simplified model: which files each step looks at is written by
hand):

```python
steps = [
    ("FROM python:3.13-slim", []),
    ("COPY requirements.txt .", ["requirements.txt"]),
    ("RUN pip install -r requirements.txt", []),
    ("COPY . .", ["app.py", "requirements.txt"]),
    ("CMD python app.py", []),
]


def rebuilt(steps, changed, cache):
    out = []
    for instruction, files in steps:
        if not cache or out or set(files) & set(changed):
            out.append(instruction)
    return out


for changed, cache in [(["app.py"], True), (["requirements.txt"], True),
                       (["app.py"], False)]:
    print(f"changed {changed[0]}, cache {cache}")
    for instruction in rebuilt(steps, changed, cache):
        print("  " + instruction)
```

```text
changed app.py, cache True
  COPY . .
  CMD python app.py
changed requirements.txt, cache True
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD python app.py
changed app.py, cache False
  FROM python:3.13-slim
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD python app.py
```

- When only `app.py` changes, two steps run with the cache; installing
  the libraries (usually the longest step) is skipped.
- When `requirements.txt` changes, the install runs again too; that is
  right.
- Without a cache everything starts over: for one line in `app.py` all
  the libraries are installed again.

In the pipeline the cache is given by `cache-from` / `cache-to`.
`type=gha` keeps the layers in GitHub's cache space (the same place as
the cache in the seventh section); `mode=max` keeps the intermediate
layers too. This is why it matters to copy `requirements.txt` and
install it first in the Dockerfile, then copy the rest of the code: the
file that changes often goes last.

## A database next to the tests: services

Some tests need a real database. GitHub Actions can open containers next
to a job: these are called **services**. A service is opened before the
job starts and deleted when the job ends.

```yaml
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/postgres
```

- `ports` opens the service's port on the machine; the tests connect to
  `localhost:5432`.
- The health check in `options` matters: a database container does not
  accept connections the moment it opens. Without the check, the tests
  can start before the database is ready and fail at random.
- The password here is not a secret: the database exists only during
  this job and cannot be reached from outside.
- The port line is in quotes: tools that read with the old YAML rules
  (for example Python's PyYAML) take values like `22:22` as a
  **base-60 number** and turn them into `1342`. Quotes close this trap in
  every tool.

## Next

In the thirteenth section we move to the case where several people work
in the same repository: branch strategy, PR checks and rules that
protect `main`.

## Summary

- With containers, the package in the "build once" rule is the image:
  build it, test inside the image, send the same image, deploy the same
  image.
- `docker/setup-buildx-action` + `docker/build-push-action`; `load: true`
  to run the image on the machine.
- Tags: the SHA on every build, `latest` on `main`, the version number
  on a version tag. Deployment uses a tag that does not change.
- You log into `ghcr.io` with `docker/login-action` and `GITHUB_TOKEN`;
  the job asks for `packages: write`. Images are not sent in PRs.
- The pipeline's machine starts from scratch every time; the layer cache
  is `cache-from` / `cache-to: type=gha`.
- `services:` opens containers such as a database next to a job;
  without a health check the tests can connect to a service that is not
  ready.
