İmaja kendi sağlık denetimini ekle. Denetim `healthcheck.py`'de hazır.

**Yapman gerekenler:**

1. `healthcheck.py`'yi de imaja kopyala (şu an yalnızca `app.py` kopyalanıyor).
2. `USER`'dan sonra bir `HEALTHCHECK` ekle: her 5 saniyede bir, 3 saniye
   zaman aşımı, 3 deneme; komut exec biçiminde `python healthcheck.py`.

Odyssey `compose.yaml` ile servisi açacak ve durumun `healthy` olmasını
bekleyecek.
