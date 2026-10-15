"Bende çalışıyor" sorunlarını erken görmek için testleri iki işletim sisteminde çalıştır:

- `test` işine matris: `os: [ubuntu-latest, windows-latest]`; makine `runs-on: ${{ matrix.os }}`.
- Biri düşünce öteki iptal edilmesin, ikisinin sonucu da görünsün: `fail-fast: false`.
