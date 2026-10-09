İşbirlikçi yöntemler geçmişe dayanır: hiç puanı olmayan yeni bir kullanıcı ya
da yeni bir ürün için ellerinde hiçbir şey yoktur. Buna **soğuk başlangıç**
(cold start) sorunu denir. Dersteki veride bunun hafif bir hâlini ölçelim:
kullanıcıları eğitimdeki puan sayılarına göre üç gruba ayırıp sapma taban
çizgisinin ve matris ayrıştırmanın (`k = 2`) test hatasına bakalım:

```python
counts = mask.sum(axis=1)
for lo, hi in ((0, 12), (12, 20), (20, 100)):
    group = [(u, i) for u, i in test if lo <= counts[u] < hi]
    row = [f"{lo}-{hi - 1}", len(group)]
    for pred in (lambda u, i: mu + bu[u] + bi[i], models[2]):
        err = np.sqrt(np.mean([(R[u, i] - pred(u, i)) ** 2 for u, i in group]))
        row.append(round(float(err), 3))
    print(*row)
```

```text
0-11 131 0.9 0.678
12-19 533 0.919 0.621
20-99 122 1.005 0.603
```

Matris ayrıştırmanın hatası, kullanıcının puanı azaldıkça büyüyor: 20 ve
üstü puanlılarda 0,603, 12'den az puanlılarda 0,678. Kişi hakkında bilgi
azaldıkça gizli vektörü de kötü öğreniliyor. Hiç puanı olmayan bir kullanıcının
vektörü hiç güncellenmez, başlangıçtaki küçük rastgele sayılarda kalır; tahmin
fiilen `μ + b_i`'ye, yani ürünün genel beğenilirliğine döner.

Gerçek sistemlerde soğuk başlangıç için birkaç yol birlikte kullanılır:

- **Popüler ya da yeni ürünler:** kişi hakkında bilgi yokken en güvenli liste.
- **Kısa bir başlangıç anketi:** "bu türlerden hangilerini seversin?"
- **İçerik bilgisi:** ürünün türü, yazarı, açıklaması; yeni ürün hiç puan
  almadan benzerlerinin yanına konabilir.
- **Örtük geri bildirim** (implicit feedback): tıklama, izleme süresi, sepete
  ekleme. Açık puandan çok daha bol; kişi puan vermese de iz bırakır.
