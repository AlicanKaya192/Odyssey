Bir gönderimde iş akışının çalışıp çalışmayacağına karar veren `should_run(branch, files, branches, ignored_dirs)` fonksiyonunu yaz:

- `branch` gönderimin dalı, `files` değişen dosyaların listesi.
- `branches` izin verilen dallar, `ignored_dirs` yoksayılan **üst klasörler** (`"docs"` gibi).
- Dal `branches` içinde değilse `False`.
- Değişen dosyalardan en az birinin üst klasörü yoksayılanlardan değilse `True`, yoksa `False`.

Bir dosyanın üst klasörü yolun ilk parçası: `"docs/setup.md"` → `"docs"`. Kökteki `"README.md"` için ilk parça kendisi.

**Beklenen çıktı:**

```
False
True
True
False
```
