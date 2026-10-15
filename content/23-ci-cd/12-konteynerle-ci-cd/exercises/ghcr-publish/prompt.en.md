The `image` job builds and tests the image. Add a `publish` job that sends the image to `ghcr.io`:

- It should start when `image` finishes, only on a push: `if: github.event_name == 'push'`. The machine is `ubuntu-latest`.
- Job permissions: `contents: read`, `packages: write`.
- Steps: get the code, `docker/setup-buildx-action@v3`, `docker/login-action@v3` (`registry: ghcr.io`, `username: ${{ github.actor }}`, `password: ${{ secrets.GITHUB_TOKEN }}`).
- The last step is `docker/build-push-action@v6`: `context: .`, `push: true`, `tags: ghcr.io/ada/greeter:${{ github.sha }}`, `cache-from: type=gha`, `cache-to: type=gha,mode=max`.
