The `image` job only gets the code. Add these steps after it:

- `docker/setup-buildx-action@v3`.
- `docker/build-push-action@v6`: `context: .`, `load: true`, `tags: greeter:test`.
- Run the tests inside the image: `docker run --rm greeter:test python -m pytest -q`.
