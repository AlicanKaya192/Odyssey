Make two changes:

- Add an `env:` section to the `test` job: the variable `APP_ENV` should get the value `test`. In place of the comment, in the same column as `runs-on`.
- Merge the two install steps (`--upgrade pip` and `requirements.txt`) into **one step**: two lines with `run: |`. Name this step `Install dependencies`.
