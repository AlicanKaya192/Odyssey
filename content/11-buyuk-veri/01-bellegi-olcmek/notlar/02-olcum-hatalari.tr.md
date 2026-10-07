Ölçmek kolay, yanlış ölçmek daha da kolay. Bu tuzakların her biri yanlış
yere yapılan bir iyileştirmeyle bitiyor.

## 1. `deep=True`'yu unutmak

`object` türlü bir sütunda `memory_usage()` yalnızca adresleri sayıyor.
Bu bölümdeki `city` sütununda fark 0,8 MB'a karşı 5,3 MB'tı. pandas 3'ün
`str` türünde fark yok ama alışkanlık olarak her zaman yaz.

## 2. Dosya boyutunu bellek sanmak

61 MB'lık CSV bellekte 96 MB tuttu; aynı dosya `object` saklamayla 252 MB.
Dosyaya bakıp "sığar" deme; birkaç bin satırı okuyup satır başına baytı
ölç, sonra satır sayısıyla çarp.

## 3. Sona bakıp tepeyi unutmak

İşlem bittiğinde tablo 4 MB olabilir ama işlem sürerken 15 MB görmüş
olabilir. Program sonda değil tepede çöker. Ağır işlemlerde `tracemalloc`
ile tepeye bak.

## 4. `tracemalloc`'u tablo ölçmek için kullanmak

`tracemalloc` pandas 3'ün metin sütunlarını görmüyor; metin ağırlıklı bir
tabloda çok küçük bir sayı verir. Tablo için `memory_usage(deep=True)`.

## 5. Süreyi bir kez ölçmek

İlk çalıştırma çoğu zaman yavaş: dosya henüz işletim sisteminin
önbelleğinde değil, modüller yükleniyor. Birkaç kez ölç, en küçüğüne ya da
ortancasına bak.

## 6. Farklı bilgisayarları karşılaştırmak

"Bende 0,8 saniye, sende 2 saniye" bir şey söylemez. İki yöntemi **aynı**
bilgisayarda, **art arda** karşılaştır; sonucu oran olarak söyle.

## 7. Birimleri karıştırmak

`1024**2` ile `10**6` arasında yaklaşık %5 fark var; büyük sayılarda
gigabaytlar kayıyor. Bir projede birimi bir kez seç, hep onu kullan.

## 8. Kopyaları hesaba katmamak

`df2 = df[df["city"] == "Istanbul"]` yeni bir tablo. Eski `df` hâlâ
bellekte. Artık kullanmayacağın büyük bir tabloyu `del df` ile bırak.

## 9. İndeksi unutmak

Karışık sayılardan kurulan indeks satır başına 8 bayt daha. Milyonlarca
satırda bu da megabaytlar demek.
