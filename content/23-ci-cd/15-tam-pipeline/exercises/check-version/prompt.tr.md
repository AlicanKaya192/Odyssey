`check_version(tag, pyproject)` fonksiyonunu yaz. `tag` etiket adı (`"v0.3.0"`), `pyproject` `pyproject.toml` dosyasının metni.

- Etiket `v` ile başlamıyorsa: `"tag 0.3.0 must start with v"` gibi döndür.
- Sürümü metinden oku: `tomllib.loads(pyproject)["project"]["version"]`.
- Etiket `"v" + sürüm` değilse: `"tag v0.3.1 does not match version 0.3.0"` gibi.
- Tutuyorsa: `"ok"`.

**Beklenen çıktı:**

```
ok
tag v0.3.1 does not match version 0.3.0
tag 0.3.0 must start with v
```
