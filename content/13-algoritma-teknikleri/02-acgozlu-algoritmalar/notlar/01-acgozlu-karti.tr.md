## Ne zaman doğru?

İki özellik birlikte gerekir:

- **Açgözlü seçim özelliği:** o an en iyi görünen seçimi yapan bir en iyi
  çözüm her zaman vardır.
- **En iyi alt yapı:** ilk seçimden sonra kalan problem aynı türden daha
  küçük bir problemdir ve onun en iyisi, bütünün en iyisinin parçasıdır.

Göstermenin yolu **değiştirme argümanı**: herhangi bir en iyi çözümü al,
ilk seçimini açgözlü seçimle değiştir, çözümün kötüleşmediğini göster.

## Çalışır mı?

| Problem | Açgözlü kural | En iyiyi verir mi? |
|---|---|---|
| Toplantı seçimi | erken biten önce | evet |
| Kesirli sırt çantası | kilo başına değer | evet |
| Bütün (0/1) sırt çantası | kilo başına değer | hayır → dinamik programlama |
| Para üstü (kanonik sistem: 1, 5, 10, 25, 50) | en büyük para | evet |
| Para üstü (`[1, 3, 4]` gibi) | en büyük para | hayır → dinamik programlama |
| Huffman kodlaması | en seyrek iki grubu birleştir | evet |
| En kısa yol (negatif kenar yok) | en yakın açılmamış düğüm (Dijkstra) | evet |
| En küçük kapsayan ağaç | en hafif kenar (Kruskal) | evet |
| Gezgin satıcı | en yakın komşuya git | hayır, yalnızca yaklaşık |

Son üç satır Algoritma Teknikleri modülünün graf bölümlerinde.

## Pratik ipuçları

- Açgözlü bir fikir aklına gelince önce **küçük bir karşı örnek** ara: 3–4
  elemanlı girdileri elle dene ya da küçük girdilerde bütün olasılıkları
  deneyen bir çözümle karşılaştır.
- Çoğu açgözlü algoritma "bir ölçüte göre sırala, sırayla bak" ya da "heap'ten
  en iyisini al" biçimindedir; maliyet çoğunlukla `O(n log n)`.
- Açgözlü sonuç en iyi olmasa bile hızlı ve çoğu zaman iyi bir **başlangıç
  noktası** ya da sınırdır (dal ve sınır yöntemlerinde).

## Sık hatalar

- Bir örnekte çalıştı diye doğru sanmak.
- Sıralama ölçütünü yanlış seçmek (toplantıda başlangıca ya da süreye göre).
- Bütün sırt çantasında kilo başına değere güvenmek.
