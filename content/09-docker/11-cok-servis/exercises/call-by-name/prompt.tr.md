`web` servisindeki istemci API'ye ulaşamıyor; günlüğü sürekli
`waiting for the API: ... Connection refused` yazıyor.

**Yapman gereken:** `web/client.py`'deki `API_URL`'i düzelt. `localhost`
`web`'in kendisi; API `api` adlı servis ve 8000'i dinliyor.

Odyssey projeyi ayağa kaldırıp `web`'in günlüğünde `items: 3` satırını
bekleyecek.
