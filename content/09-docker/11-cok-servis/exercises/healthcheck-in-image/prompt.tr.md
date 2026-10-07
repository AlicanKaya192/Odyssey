compose.yaml `web`'i `api` sağlıklı olunca başlatıyor, ama `api`'nin sağlık
denetimi yok; Compose şunu diyor: `container ... has no healthcheck
configured`.

**Yapman gereken:** denetimi compose.yaml'a değil, **API'nin imajına**
`HEALTHCHECK` talimatıyla yaz (`api/Dockerfile`): 2 saniye arayla, 3 saniye
zaman aşımıyla, 15 deneme; komut yorumdaki Python satırı. Uzun satırı `\`
ile bölebilirsin.

Odyssey projeyi ayağa kaldırıp `web`'in günlüğünde `items: 3`'ü arayacak.
