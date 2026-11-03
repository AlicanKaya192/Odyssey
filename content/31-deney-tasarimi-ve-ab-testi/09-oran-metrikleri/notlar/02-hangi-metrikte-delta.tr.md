Sorulacak tek soru: **metriğin paydası atama birimi mi?**

## Payda atama birimiyse: sıradan test

- Kullanıcıyla atanmış testte **kullanıcı başına** satın alma oranı
  (satın alan kullanıcı / kullanıcı). Her kullanıcı bir deneme; oran testi
  ya da Welch yeter.
- Kullanıcı başına gelir, kullanıcı başına dakika. Kullanıcı düzeyinde bir
  sayı; Welch ya da bootstrap.

## Payda başka bir şeyse: delta yöntemi

- Gösterim başına tıklama (CTR).
- Sipariş başına gelir (ortalama sepet): sipariş sayısı kullanıcıdan
  kullanıcıya değişir.
- Oturum başına süre, oturum başına sayfa.
- Arama başına tıklama.

Bunların hepsinde aynı kullanıcının birden çok gösterimi, siparişi ya da
oturumu var ve bunlar birbirine benziyor.

## Aynı fikir başka yerlerde

- **Küme halinde atama:** mağaza ya da şehir bazında atanan bir testte
  birim mağazadır; içindeki müşteriler bağımsız sayılmaz.
- **Paydanın kendisi değişebilir:** B kullanıcıların daha çok sayfa
  görmesini sağlıyorsa oranın paydası da değişir. Oran düşmüş görünürken
  toplam tıklama artmış olabilir; payı ve paydayı ayrı ayrı da raporlayın.

## Hızlı denetim

Bir oran metriğinin testini A/A verisiyle birkaç yüz kez çalıştırın:
yanlış alarm %5'i belirgin biçimde aşıyorsa birimi yanlış sayıyorsunuzdur.
