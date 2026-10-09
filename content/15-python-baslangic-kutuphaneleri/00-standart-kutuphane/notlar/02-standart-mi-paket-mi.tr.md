Bir işi standart kütüphaneyle mi, `pip` ile kurulan bir paketle mi
yapmalısın? Kısa kural: **önce standart kütüphaneye bak**, yetmiyorsa paket
kur.

## Standart kütüphanenin artısı

- Kurulum yok: betik Python olan her bilgisayarda çalışır.
- Sürüm sorunu yok: Python'la birlikte güncellenir, belgesi tek yerde.
- Küçük işler için fazlasıyla yeterli: bir CSV okumak, bir klasördeki
  dosyaları saymak, iki tarih arasındaki günü bulmak için pandas gerekmez.

## Paketin artısı

- Büyük veriyle hız: bir milyon satırlık hesapta NumPy ve pandas saf
  Python'dan çok daha hızlıdır (Algoritmalar patikasında ölçtük).
- Hazır yetenek: makine öğrenmesi (scikit-learn), grafik (Matplotlib),
  HTTP isteği için `requests` gibi.

## Bir paketi kullanmadan önce

- Gerçekten gerekli mi? Tek bir küçük fonksiyon için koca bir paket eklemek,
  projeyi kuracak herkese yük getirir.
- Bakımı sürüyor mu? Son sürümün tarihine ve belgesine bak.
- Hangi sürüm? `requirements.txt` içinde sürümü sabitle (`pandas==3.0.6`
  gibi); Python patikasının Paketler ve Ortamlar bölümünde anlatıldı.

## Ad çakışmasına dikkat

Kendi dosyana standart kütüphanedeki bir modülün adını verme: `random.py`
adında bir dosya yazarsan, aynı klasördeki `import random` artık senin
dosyanı içe aktarır ve `random.randint` "yok" der. Hata mesajı garip görünür,
sebebi dosya adıdır.
