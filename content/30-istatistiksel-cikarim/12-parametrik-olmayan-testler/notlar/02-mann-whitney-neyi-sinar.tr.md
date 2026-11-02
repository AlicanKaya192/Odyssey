Mann–Whitney testi sık sık "medyanları karşılaştıran test" diye anlatılır.
Bu tam doğru değil ve yanlış sonuca götürebilir.

## Gerçek sorusu

"Rastgele bir B değeri, rastgele bir A değerinden büyük olmaya **yatkın**
mı?" Yani $P(B > A)$ 0,5'ten farklı mı?

- İki grubun dağılımlarının **biçimi aynıysa** ve biri ötekinin kaydırılmış
  hâliyse, bu soru medyanların farkına denk gelir.
- Biçimler farklıysa (biri çok yayılmış, öteki toplu) medyanlar aynı olsa
  bile test anlamlı çıkabilir; ya da medyanlar farklıyken anlamlı
  çıkmayabilir.

## Ortalama hakkında konuşmaz

Toplam gelir gibi bir **ortalama** sorusu soruyorsan Mann–Whitney doğru araç
değildir. Birkaç dev sipariş ortalamayı ve dolayısıyla geliri gerçekten
değiştirir; sıralı test onları bilerek "küçültür". Gelir testi için büyük
örneklemde t-testi ya da bootstrap kullanılır.

## Ne zaman tam yerinde?

- Çarpık bir metrikte "tipik kullanıcı daha iyi durumda mı?" sorusu.
- Küçük örneklem ve aykırı değerler.
- Sıralı (ordinal) veri: 1–5 arası memnuniyet puanı gibi, aralarındaki
  uzaklığın anlamı belirsiz olan ölçekler.

## Raporlarken

p'nin yanına ortak dil etki büyüklüğünü ($U / n_A n_B$) ve iki grubun
medyanlarını yaz. "B'nin medyanı daha yüksek ve rastgele bir B siparişi
rastgele bir A siparişinden %57 olasılıkla büyük" cümlesi p'den çok daha
anlaşılırdır.
