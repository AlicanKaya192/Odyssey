Python matematik yapabiliyor; ama Python bilmeyenler de yapabilsin. Kullanıcıdan bir aritmetik ifade isteyen, sonucu hesaplayan ve **virgülden sonra tek basamaklı** bir ondalıklı sayı olarak yazan bir program yaz. Girdinin `x y z` biçiminde olduğunu varsayabilirsin (aralarında birer boşluk): `x` bir tam sayı, `y` `+`, `-`, `*` ya da `/`, `z` bir tam sayı. `1 + 1` için `2.0`. `y` `/` ise `z` sıfır olmayacak. (CS50'de dosyanın adı `interpreter.py`.)

İpucu (CS50'den): dizelerin `split` metodu metni parçalara ayırır ve parçalar tek satırda değişkenlere atanabilir: `x, y, z = expression.split(" ")` ifadesi `"1 + 1"` için `x`'e `"1"`, `y`'ye `"+"`, `z`'ye `"1"` atar.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `1 + 1` → çıktı `2.0`
- Girdi `2 - 3` → çıktı `-1.0`
- Girdi `2 * 2` → çıktı `4.0`
- Girdi `50 / 5` → çıktı `10.0`
- Girdi `7 / 2` → çıktı `3.5`
