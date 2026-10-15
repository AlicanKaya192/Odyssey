This pipeline builds the package on every push to `main`. It should run only on a version tag and a package with the wrong number should not be built:

- Instead of the `main` branch, only tags starting with `v` should start the pipeline (`tags: ["v*"]`).
- The number check should run **before** the build: `python scripts/check_version.py "$GITHUB_REF_NAME"`.
