Bu API'de oturumu kapatan uç nokta `GET` ile yazılmış. Bir tarayıcı
sayfayı önceden yüklerken (bazı tarayıcılar bağlantıları önceden açar)
kişinin oturumu kendiliğinden kapanabilir.

**Yapman gereken:** oturumu kapatmak durumu değiştiriyor; uç noktayı doğru
yönteme taşı.

```text
GET  /logout   405
POST /logout   {"logged_in": false}
```
