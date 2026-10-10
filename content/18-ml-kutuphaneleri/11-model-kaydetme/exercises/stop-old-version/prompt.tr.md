`stop_old_version(version)` modeli `version` sürümünde kaydedilmiş gibi
gösteren bir dosya hazırlayıp yüklüyor. Yükleme sırasında
`InconsistentVersionWarning` **hataya çevrilsin** (`warnings.catch_warnings()`
içinde `simplefilter("error", ...)`), böylece `except` kolu çalışıp
`[model_adı, eski_sürüm]` dönsün. Başlangıç kodunda uyarı yalnızca uyarı
olarak kalıyor ve yükleme devam ediyor.

**Beklenen çıktı:**

```
['LogisticRegression', '1.2.2']
```
