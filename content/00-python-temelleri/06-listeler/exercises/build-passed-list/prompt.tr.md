Bir sınav sonucu listesi verilmiş:

```python
scores = [45, 82, 67, 30, 95, 58]
```

60 ve **üzeri** olan sonuçlardan **yeni bir liste** kur. Adı `passed` olsun.

Sonra hem listeyi hem de kaç kişinin geçtiğini yazdır. Beklenen çıktı:

```
[82, 67, 95]
3
```

Yöntem şu: boş bir liste ile başla, asıl liste üzerinde dön, şartı sağlayan
her elemanı yeni listeye `append` et.

> `60 ve üzeri` deniyor, yani `>=` kullanacaksın. `>` yazarsan tam 60 alan biri
> listeye girmez. Bu örnekte tam 60 yok ama alışkanlığı doğru kurmak önemli.
