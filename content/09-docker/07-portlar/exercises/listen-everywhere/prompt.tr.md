Bu küçük API konteynerde çalışıyor, port da yayınlanıyor; ama dışarıdan
istek atınca `Empty reply from server` geliyor.

**Yapman gereken:** `server.py`'de sunucunun dinlediği adresi düzelt:
konteynerin içinde program **bütün adresleri** dinlemeli. (Ekrana yazdırılan
satırı da aynı adresle güncelle.)

Odyssey `/health` adresine istek atacak; yanıt `{"status": "ok"}` olmalı.
