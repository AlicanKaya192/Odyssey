To catch "it works on my machine" problems early, run the tests on two operating systems:

- A matrix on the `test` job: `os: [ubuntu-latest, windows-latest]`; the machine is `runs-on: ${{ matrix.os }}`.
- When one fails the other should not be cancelled, so both results are visible: `fail-fast: false`.
