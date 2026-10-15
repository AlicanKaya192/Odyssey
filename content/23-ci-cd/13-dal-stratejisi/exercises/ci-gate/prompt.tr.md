Zorunlu listeye tek bir ad koymak için bir `ci-ok` işi ekle:

- `lint` ve `test` işlerine bağlı olsun, onlar düşse de çalışsın: `if: always()`. Makine `ubuntu-latest`.
- İlk adım `exit 1`; yalnızca bağlı işlerden biri düştüyse ya da iptal edildiyse çalışsın: `needs.*.result` içinde `'failure'` ya da `'cancelled'` (`contains(...)`).
- İkinci adım bir `echo`.
