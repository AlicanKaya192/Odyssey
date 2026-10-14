Hattın kapıları ölçümlerini bir sözlüğe yazmış:

- `"syntax"`: sözdizimi kapısının çıkış kodu
- `"format"`: biçim kapısının çıkış kodu
- `"lint_errors"`: lint hata sayısı
- `"coverage"`: kapsam yüzdesi

İki fonksiyon yaz:

- `failed_gates(results, min_coverage)`: kapanan kapıların adlarını bu sırayla bir listede döndür: `"syntax"`, `"format"`, `"lint"`, `"coverage"`. Çıkış kodu `0` değilse, lint hatası varsa ya da kapsam `min_coverage`'ın altındaysa kapı kapanır.
- `gate_message(failed)`: liste boşsa `"PASS"`, değilse `"FAIL: format, lint"` gibi.

Adları virgül ve boşlukla birleştirmek için `", ".join(liste)` kullanılabilir.

**Beklenen çıktı:**

```
[]
['format', 'lint', 'coverage']
PASS
FAIL: format, lint, coverage
```
