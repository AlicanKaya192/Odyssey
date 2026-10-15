İki iş ekle:

- `build`: `test` bitince, `ubuntu-latest`. Kodu çek, Python 3.13 kur, `python -m pip install build`, `python -m build`, sonra `actions/upload-artifact@v4` ile `name: dist`, `path: dist/`.
- `ci-ok`: `lint`, `test` ve `build`'e bağlı, `if: always()`, `ubuntu-latest`. İlk adım `exit 1`, yalnızca `needs.*.result` içinde `'failure'` ya da `'cancelled'` varsa; ikinci adım bir `echo`.
