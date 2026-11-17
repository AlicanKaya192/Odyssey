Karışıklık matrisinin bir **satırı** o rakamın gerçek örneklerinin nereye
gittiğini, bir **sütunu** modelin o rakam dediği örneklerin nereden geldiğini
gösterir:

```python
print("3:", matrix[3].tolist())
print("8:", matrix[8].tolist())
print("col 8:", matrix[:, 8].tolist())
for digit in range(10):
    row = matrix[digit]
    if row[digit] < row.sum():
        print(digit, round(100 * row[digit].item() / row.sum().item(), 1))
```

```text
3: [0, 0, 1, 31, 0, 0, 0, 0, 4, 0]
8: [0, 0, 0, 0, 0, 0, 0, 0, 38, 0]
col 8: [0, 2, 0, 4, 0, 0, 0, 0, 38, 0]
1 94.6
3 86.1
4 97.4
5 94.7
7 97.6
9 97.4
```

- 3 satırı: 36 gerçek 3'ün 31'i doğru, 4'ü 8'e, 1'i 2'ye gitmiş.
- 8 sütunu: model "8" dediği 44 resmin 4'ünde aslında 3, 2'sinde 1
  görüyordu.
- Son döküm yalnızca hatası olan rakamların sınıf başına doğruluğunu
  yazıyor. En düşüğü %86,1 ile 3. Bir sınıfın oranı ötekilerden belirgin
  düşükse, o sınıfın yanlış tahmin edilen örneklerine tek tek bakmak iyi
  bir sonraki adımdır.
- Sınıf başına doğruluğun satır toplamına bölündüğüne dikkat: bu, o
  sınıfın **duyarlılığı** (recall).
