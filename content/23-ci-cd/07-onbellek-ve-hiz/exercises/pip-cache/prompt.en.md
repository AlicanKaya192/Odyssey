All packages are downloaded again on every run. Add an `actions/cache@v4` step **before** the installation:

- `path`: `~/.cache/pip`
- `key`: `pip-`, the operating system (`runner.os`) and the hash of `requirements.txt` (`hashFiles`)
- `restore-keys`: if there is no full key, the newest cache with the prefix `pip-<operating system>-`
