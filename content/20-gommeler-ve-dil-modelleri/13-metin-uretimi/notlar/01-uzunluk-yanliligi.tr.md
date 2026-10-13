Bir cümlenin log olasılığı, kelimelerinin log olasılıklarının toplamıdır ve
her kelime toplamı biraz daha eksiye götürür. Bu yüzden ışın araması kısa
cümleleri kayırır: "hey there , the app ." gibi bir cümle, uzun ve bilgi
dolu bir talepten neredeyse her zaman daha olasıdır. Çare **uzunluk normalleştirme**
(length normalization): yolları sıralarken puanı `uzunluk ** alpha`'ya
bölmek. Dersteki `beam_search` bunu `alpha` ile yapıyor; `alpha = 0`
normalleştirme yok, `alpha = 1` kelime başına ortalama.

```python
pad = "    "
for alpha in [0.0, 0.5, 1.0]:
    score, text = beam_search(50, alpha)
    print(alpha, len(text.split()), score)
    print(textwrap.fill(text, 76, initial_indent=pad, subsequent_indent=pad))
```

```text
0.0 12 -7.27
    hello , the parcel arrived damaged and the box was open .
0.5 17 -7.92
    good morning , the parcel arrived damaged and the box was open . this is
    urgent !
1.0 28 -10.16
    i get error e# when i log in on the app crashes every time i open the
    order page . i have been a customer for # years
```

- Normalleştirme arttıkça ışın daha uzun cümleleri seçiyor; toplam log
  olasılık düşüyor ama kelime başına olasılık artıyor (−7,27 / 13 ≈ −0,56,
  −10,16 / 29 ≈ −0,35).
- `alpha = 1` fazla ileri gidiyor: cümle 30 kelimelik sınıra kadar uzayıp
  yarıda kaldı ("for # years" ile bitiyor). Uzunluğu tamamen ödüllendirmek de
  bir yanlılık.
- Hangi `alpha`'nın iyi olduğu işe bağlı: makine çevirisinde çeviri
  kaynaktan çok kısa çıkmasın diye 0,6–1 arası değerler yaygın.
- Ders: "en olası cümle" çoğu zaman istediğimiz cümle değildir. Kod çözme
  yöntemi, modelin olasılığı ile gerçekten istediğimiz metin arasındaki
  farkı kapatmaya çalışır.
