**The pipeline's flow**

Build → test inside the image → send the same image to the registry →
deploy the same image.

**Actions**

| Action | What it does |
|---|---|
| `docker/setup-buildx-action@v3` | Prepares the builder (Buildx) |
| `docker/build-push-action@v6` | Builds the image; sends it with `push: true` |
| `docker/login-action@v3` | Logs into the image registry |

**`build-push-action` settings**

| Setting | Meaning |
|---|---|
| `context: .` | The build uses the repository root |
| `tags:` | The image's name and tag |
| `load: true` | Load the image into the machine's Docker (for `docker run`) |
| `push: true` | Send the image to the registry |
| `cache-from: type=gha` | Take layers from GitHub's cache |
| `cache-to: type=gha,mode=max` | Write layers to the cache (intermediate layers included) |

**Build and test in the image**

```yaml
      - uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: greeter:test
      - run: docker run --rm greeter:test python -m pytest -q
```

**Send to `ghcr.io`**

```yaml
    permissions:
      contents: read
      packages: write
    steps:
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

- In a PR build and test, **do not send**: `if: github.event_name == 'push'`.
- The image name is lowercase.

**The job itself in a container**

```yaml
  lint:
    runs-on: ubuntu-latest
    container: python:3.13-slim
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install ruff
      - run: python -m ruff check .
```

`container:` runs all of the job's steps inside that image; `services:`
opens separate containers **next to** the job.
