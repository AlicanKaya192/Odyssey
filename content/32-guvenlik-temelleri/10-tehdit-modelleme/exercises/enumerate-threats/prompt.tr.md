`PER_ELEMENT` tablosu başlangıç kodunda hazır. `elements` `[ad, tur]`
listelerinden oluşuyor.

`enumerate_threats(elements)` her parça için sorulacak tehditleri
`"ad:HARF"` metinleri olarak döndürsün: parçalar listedeki sırayla, harfler
tablodaki sırayla.

Tablonun bilmediği bir tür gelirse onu **süreç gibi** ele al (altı harfin
hepsi): emin olamıyorsan daha çok soru sor.

**Beklenen çıktı:**

```
11
student:S
student:R
login:T
login:I
login:D
plugin:S
plugin:T
plugin:R
plugin:I
plugin:D
plugin:E
```
