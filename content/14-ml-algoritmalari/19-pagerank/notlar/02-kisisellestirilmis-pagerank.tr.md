Derste gezgin sıkılınca **herhangi bir** sayfaya atlıyordu (`(1 − d) / n`).
Atlama yalnızca belirli sayfalara yapılırsa **kişiselleştirilmiş PageRank**
(personalized PageRank) elde edilir: sonuç artık "genel olarak önemli" değil,
"şu sayfaya yakın ve önemli" sayfaları gösterir. Öneri sistemlerinde ve
"buna benzer" aramalarında kullanılır.

Dersteki `M` ile, gezgin sıkılınca hep D'ye dönsün:

```python
v = np.zeros(n)
v[idx["D"]] = 1                          # atlama yalnızca D'ye
rp = np.full(n, 1 / n)
for _ in range(200):
    rp = 0.85 * M @ rp + 0.15 * v
print(show(rp))
print(show(pagerank(M)[0]))
```

```text
A=0.292 B=0.124 C=0.343 D=0.150 E=0.064 F=0.027
A=0.347 B=0.173 C=0.379 D=0.025 E=0.036 F=0.040
```

Genel PageRank'te D'nin değeri 0,025, kişiselleştirilmişte 0,15: gezgin
oraya sürekli geri dönüyor. E 0,036'dan 0,064'e çıkıyor, çünkü D'nin doğrudan
komşusu. F ise 0,040'tan 0,027'ye iniyor: D'den iki adım uzakta ve genel
PageRank'te aldığı rastgele atlama payını artık almıyor. A, B ve C'nin
sırası değişmiyor; D'nin bağlantıları da sonunda onlara akıyor.

Bir öneri sisteminde `v`, kişinin beğendiği ürünlerin üzerine dağıtılır;
yüksek değer alan ama kişinin henüz görmediği düğümler önerilir.
