The package should also be uploaded to PyPI, but without a stored key (trusted publishing). Add a `publish` job:

- It should start when `build` finishes; the machine is `ubuntu-latest`.
- It should be tied to the `pypi` environment (`environment: pypi`).
- It should get only the `id-token: write` permission.
- It should download the `dist` artifact into the `dist` folder.
- It should run the `pypa/gh-action-pypi-publish@release/v1` action.
