Bölüm 07'de ağaç `age` sütununa **0.0** önem vermişti ve "bu sütun
işe yaramıyor" sonucu çıkarmanın neden yanlış olduğunu konuşmuştuk.
Şimdi ormanın ne dediğine bakacaksın.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır.
2. İki modeli eğit: `tree` (`max_depth=2`) ve `forest` (200 ağaç), ikisi de
   `random_state=42`.
3. Her biri için tek satır yazdır: **ad ve üç önem değeri** yan yana
   (sütun sırasıyla `age`, `income`, `visits`; üç ondalık).
4. Son satırda kaç sütunun **tam olarak sıfır** önem aldığını yan yana
   yazdır: önce ağaçta, sonra ormanda.

**Beklenen çıktı:**

```
tree 0.0 0.454 0.546
forest 0.232 0.344 0.424
1 0
```

**Ağaç `age` sütununa 0.0 diyor, orman 0.232.**

Ağaç haksız değil: derinlik 2'lik bir ağaçta yalnızca üç bölünme var ve
`visits` ile `income` daha erken kazandı. `age` hiç denenmedi bile.

**Ormanda 200 ağaç var** ve her biri her bölünmede özelliklerin yalnızca
bir alt kümesini deniyor (`max_features`). Bu, `age`'in defalarca **tek
başına** yarıştığı anlamına geliyor — `visits` o bölünmede saklandığında
sıra ona geliyor. Gerçek katkısı böyle ortaya çıkıyor.

**Son satır özet: ağaçta bir sütun sıfır, ormanda hiçbiri.**

**Alınacak ders:** tek bir ağacın "bu sütun önemsiz" demesi güvenilmez. Sıfır
önem, "katkısı yok" değil "sırası gelmedi" anlamına gelebiliyor.

**Ama üç tuzak hâlâ duruyor:**

1. Önem **sebep** demek değil — orman da bunu değiştirmiyor.
2. İlişkili sütunlar hâlâ önemi paylaşıyor.
3. Çok değerli sütunlar hâlâ şişiyor.

Daha güvenilir yol yine `permutation_importance`: sütunu karıştırıp skorun
ne kadar düştüğüne bakıyor ve test kümesinde ölçülebiliyor.
