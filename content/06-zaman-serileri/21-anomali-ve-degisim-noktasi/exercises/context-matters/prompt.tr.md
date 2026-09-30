Pompa basıncında bakım defterindeki 12 olayı bul: önce bütün seriye z-skoruyla,
sonra saatin ortancasından sapmayla.

Başlangıç kodunda `p` (basınç), `events` (olay saatleri) ve `calm` (son hafta
hariç seri) hazır.

**Yapman gerekenler:**

1. `calm` üzerinde z-skoru hesapla. Mutlak değeri 3'ü geçen saatleri
   `"%m-%d %H"` listesi olarak ve bunların kaçının `events` içinde olduğunu
   aynı satıra yazdır.
2. 5 Eylül 03:00 için: değeri, z-skorunu (bir ondalık) ve o saatin (03:00)
   `calm` içindeki ortancasını aynı satıra yazdır.
3. Her saatin ortancasından bir profil çıkar
   (`calm.groupby(calm.index.hour).median()`), kalıntıyı hesapla ve dayanıklı
   puanı kur: `0.6745 * (kalıntı - ortanca) / MAD`.
4. Puanı mutlak değerce 3'ü geçen saat sayısını ve bunların kaçının `events`
   içinde olduğunu aynı satıra yazdır.
5. İşaretlenen ama `events` içinde **olmayan** saatlerin günlerini (`"%m-%d"`,
   tekrarsız, sıralı) liste olarak yazdır.

**Beklenen çıktı:**

```
['09-03 14'] 1
5.89 -0.2 5.22
20 12
['09-30']
```

Bütün seriye bakan kural 12 olayın birini görüyor; saatin bağlamını bilen kural
hepsini. 5 Eylül 03:00'teki değer ortalamanın hemen yanında, ama o saat için
0.67 bar fazla. Defterde olmayan sekiz işaretin hepsi aynı günde: o gün başka
bir şey olmuş (derste: takılı sensör).
