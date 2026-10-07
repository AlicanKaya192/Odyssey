Bir API'yi kullanmadan önce belgesinde bu soruların cevabını ara. Cevabını
bulamadığın her soru, ileride bir hata olarak karşına çıkar.

## Okuma listesi

1. **Adres nedir?** API'nin ana adresi (örneğin
   `https://api.example.com`). Bütün uç noktalar bunun arkasına eklenir.
2. **Hangi uç noktalar var?** Her birinin adı ve ne işe yaradığı:
   `/weather` şu anki hava, `/forecast` sonraki günler.
3. **Her uç nokta ne istiyor?** Zorunlu bilgiler (`city`) ve isteğe
   bağlı olanlar (`units=metric`).
4. **Yanıt neye benziyor?** Belgede genellikle örnek bir yanıt olur. Hangi
   alanlar geliyor, sayılar hangi birimde?
5. **Kimlik gerekiyor mu?** Birçok API "anahtar" (API key) ister. Anahtarın
   nereye yazılacağı belgede yazar. Bunu Bölüm 08'de göreceğiz.
6. **Sınırlar ne?** Dakikada ya da günde kaç istek atılabileceği. Aşılırsa
   sunucu bir süre cevap vermeyi keser.
7. **Hangi hatalar gelebilir?** "Şehir bulunamadı", "anahtar geçersiz" gibi
   durumlarda ne yanıt geldiği.

## Belge örneği

Hayali bir hava durumu API'sinin belgesinden bir parça:

```text
GET /weather
  city   (zorunlu)  Şehir adı, örnek: Istanbul
  units  (isteğe bağlı)  metric | imperial, varsayılan metric

Yanıt 200:
  {"city": "Istanbul", "temp": 18, "sky": "cloudy"}

Yanıt 404:
  {"error": "unknown city"}
```

Bu kadarından şunları öğreniyorsun: uç nokta `/weather`, `city` vermeden
sormak işe yaramaz, sıcaklık varsayılan olarak santigrat, bilinmeyen bir
şehir için `404` ve bir hata mesajı geliyor.

## Belge yoksa ya da eksikse

- Örnek yanıtları dikkatle oku; alan adları çoğu şeyi anlatır.
- Küçük bir deneme isteği at ve yanıta bak (bunu araçlarla nasıl yapacağını
  Bölüm 14'te göreceksin).
- Belgedeki tarih ve sürüm numarasına bak: eski bir belge, değişmiş bir
  API'yi anlatıyor olabilir.
