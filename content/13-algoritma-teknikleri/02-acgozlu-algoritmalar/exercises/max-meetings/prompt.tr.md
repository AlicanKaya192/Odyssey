`max_meetings(meetings)` fonksiyonunu yaz: tek odaya sığabilecek en çok
toplantı sayısını döndürsün. Her toplantı `[başlangıç, bitiş]`; bir toplantı
öbürünün bittiği anda başlayabilir.

**Erken biten önce:** bitişe göre sırala, son seçilenin bitişini tut,
başlangıcı ondan önce olmayanı al.

Son satırdaki 200 000 istek, her yeni toplantıyı seçilenlerin hepsiyle
karşılaştıran bir çözümü süre sınırına takar.

**Beklenen çıktı:**

```
3
2
8201
```
