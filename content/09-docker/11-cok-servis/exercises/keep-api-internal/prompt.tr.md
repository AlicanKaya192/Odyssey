Bu projede dışarıdan yalnızca vitrin (`web`) görülmeli. `api` aynı ağdaki
servislere hizmet veriyor; ona bilgisayardan ulaşılması gerekmiyor ama
dışarıya açılmış.

**Yapman gereken:** `api` servisinin `ports:` satırlarını kaldır. `web`'inki
kalsın.

Odyssey projeyi ayağa kaldırıp vitrine ve **ağın içinden** API'ye istek
atacak; ikisi de çalışmalı.
