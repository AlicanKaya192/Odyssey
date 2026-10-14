YAML okununca iş akışı iç içe bir sözlük olur. `WORKFLOW` bu sözlüğün hazır hâli.

`job_summary(workflow)` fonksiyonunu yaz. Her iş için bir satırlık metni sırayla bir listede döndür:

- `"test: windows-latest, 3 steps"`

Yani: işin adı, `runs-on` değeri ve adım sayısı.

- İşler `workflow["jobs"]` sözlüğünde.
- `.items()` hem adı hem değeri verir.

**Beklenen çıktı:**

```
lint: ubuntu-latest, 2 steps
test: windows-latest, 3 steps
```
