`test` işini iki işletim sistemi ve iki Python sürümüne yay, sonra bir kapı ekle:

- Matris: `os: [ubuntu-latest, windows-latest]`, `python: ["3.12", "3.13"]`; Windows'ta 3.12'yi çıkar (`exclude`). `fail-fast: false`. Makine `${{ matrix.os }}`.
- `setup-python`: `python-version: ${{ matrix.python }}`, `cache: pip`.
- `ci-ok` işi: `test`'e bağlı, `if: always()`, `ubuntu-latest`; ilk adım `exit 1`, yalnızca `needs.*.result` içinde `'failure'` ya da `'cancelled'` varsa; ikinci adım bir `echo`.
