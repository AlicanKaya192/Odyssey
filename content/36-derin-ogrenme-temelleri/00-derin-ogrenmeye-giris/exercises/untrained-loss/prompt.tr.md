Bütün sınıflara eşit puan veren bir model hiçbir şey bilmiyor demektir.
`untrained_loss(n_classes)` 4 örnek için sıfırlardan oluşan puanları
(`torch.zeros(4, n_classes)`) ve 0 etiketlerini `nn.CrossEntropyLoss`'a versin;
kaybı 3 basamakla döndürsün. Sonucu dersteki ilk kayıpla (2,33) karşılaştır.

**Beklenen çıktı:**

```
2.303
1.099
```
