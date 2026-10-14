`chat_cost(price_in, price_out)` başlangıç kodundaki üç soruyu
`ChatClient(REPLIES)` ile, her çağrıda **bütün geçmişi** göndererek sorsun
(sistem mesajı yok; her cevabı geçmişe `assistant` mesajı olarak ekle,
`max_tokens=50`). Cevapların `input_tokens` ve `output_tokens` toplamlarını
ve milyon token başına verilen fiyatlarla maliyeti döndürsün:
`[giren toplam, çıkan toplam, maliyet]`; maliyet 8 basamağa yuvarlanmış
`float`.

**Beklenen çıktı:**

```
[97, 17, 7.4e-05]
[97, 17, 0.00033]
```
