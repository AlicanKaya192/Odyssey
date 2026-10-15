`tests/test_shop.py`'deki bir test `@pytest.mark.flaky` ile işaretli. Onu ana hattan ayır:

- `test` işi işaretli testleri dışarıda bıraksın: `python -m pytest -q -m "not flaky"`.
- Yeni bir `quarantine` işi (`ubuntu-latest`) kodu çeksin, paketleri kursun ve yalnızca işaretli testleri çalıştırsın: `python -m pytest -q -m flaky`.
- `quarantine` düşse de çalışma kırmızı olmasın: `continue-on-error: true`.
