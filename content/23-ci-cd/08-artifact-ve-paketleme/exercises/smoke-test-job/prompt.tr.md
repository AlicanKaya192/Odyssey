Paketin kurulunca çalıştığını deneyen bir `smoke-test` işi ekle:

- `build` bitince başlasın, makine `ubuntu-latest`.
- Kodu **çekmesin**; Python 3.13'ü kursun.
- `dist` artifact'ini `dist` klasörüne indirsin.
- `pip install dist/*.whl` ile kursun.
- `python -c "import greeter; print(greeter.hello())"` çalıştırsın.
