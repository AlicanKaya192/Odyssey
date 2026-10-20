Kapı yalnızca çekme isteklerinde çalışıyor. Hiç değişiklik olmasa da kütüphaneler ve veri değişebildiği için haftada bir de çalışsın:

- Her **pazartesi 06:00 UTC**'de (`schedule`) ve Actions sekmesinden elle (`workflow_dispatch`). `pull_request` tetikleyicisi yerinde kalsın.
- `model-gate` işinin sonuna ölçümleri saklayan bir adım ekle: `actions/upload-artifact@v4`, **her durumda** çalışsın, `name: metrics`, `path: metrics.json`.
