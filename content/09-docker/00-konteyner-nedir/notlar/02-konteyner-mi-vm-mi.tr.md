Konteyner ile sanal makine aynı soruya iki farklı cevap: "bir programı
bilgisayarın geri kalanından nasıl ayırırım?" İkisini yan yana koyalım.

## Karşılaştırma

| | Sanal makine | Konteyner |
|---|---|---|
| Ne taklit ediliyor? | Bütün bir bilgisayar | Yalnızca programın çevresi |
| İçinde işletim sistemi | Tam bir işletim sistemi, kendi çekirdeğiyle | Yok; ana makinenin çekirdeği ortak |
| Boyut | Genellikle birkaç GB | Çoğu zaman onlarca–yüzlerce MB |
| Açılış süresi | Dakikalar | Saniyeden kısa |
| Bir sunucuya sığan | Birkaç–on tane | Yüzlerce |
| Ayrılık | Çok güçlü | Güçlü ama çekirdek ortak |

## Neden bu kadar küçük?

Sanal makine açıldığında içindeki işletim sistemi de baştan açılıyor:
sürücüler, servisler, bellek yönetimi. Konteyner açıldığında ise yalnızca
**bir program** başlıyor; işletim sisteminin geri kalanı zaten ana makinede
çalışıyor.

Konteynerin içindeki "Linux dosyaları" (ör. `python:3.13-slim` içindeki)
bir işletim sistemi değil, programın ihtiyaç duyduğu **komutlar ve
kütüphaneler**: `ls`, `sh`, birkaç C kütüphanesi. Çekirdek bunların içinde
yok.

## Windows'ta neden yine bir sanal makine var?

Konteyner ana makinenin çekirdeğini kullanıyor. Linux konteynerleri bir
**Linux çekirdeği** istiyor; Windows'un çekirdeği Linux değil. Docker
Desktop bu yüzden arka planda küçük bir Linux sanal makinesi çalıştırıyor
(WSL 2 ile) ve bütün konteynerler onun içinde, onun çekirdeğini ortak
kullanıyor.

Yani Windows'ta tek bir küçük sanal makine var, konteynerler onun içinde.
Yüz konteyner için yüz sanal makine değil.

## Hangisi ne zaman?

**Konteyner** seç:

- bir programı başka bilgisayarlarda aynı çalıştırmak istiyorsan,
- birden çok küçük servisi yan yana çalıştıracaksan,
- hızlı açılıp kapanması önemliyse.

**Sanal makine** seç:

- başka bir işletim sistemini bütünüyle denemek istiyorsan (Linux'ta
  Windows çalıştırmak gibi),
- çok sıkı bir ayrılık gerekiyorsa (güvenmediğin kod),
- masaüstü olan bir sistem gerekiyorsa.

Gerçekte ikisi çoğu zaman birlikte: bulutta kiralanan sunucu bir sanal
makine, üzerinde de konteynerler çalışıyor.
