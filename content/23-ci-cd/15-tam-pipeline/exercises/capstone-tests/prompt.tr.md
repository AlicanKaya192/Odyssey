Hatta yalnızca `lint` var. Bir `test` işi ekle:

- `lint` bitince başlasın, makine `ubuntu-latest`, `timeout-minutes: 15`.
- Matris: `python: ["3.12", "3.13"]`, `fail-fast: false`.
- Adımlar: kodu çek; `actions/setup-python@v5` (`python-version: ${{ matrix.python }}`, `cache: pip`); `python -m pip install -r requirements-dev.txt`; `python -m pytest -q --cov=tempconv --cov-fail-under=90`.
