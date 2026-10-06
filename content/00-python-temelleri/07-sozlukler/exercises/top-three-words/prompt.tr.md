Bir metnin kelimeleri liste olarak verilmiş:

```python
words = ["the", "cat", "and", "the", "dog", "and", "the", "bird", "sat", "on", "the", "mat"]
```

1. Her kelimenin kaç kez geçtiğini `counts` sözlüğünde say
   (`{"the": 4, "cat": 1, ...}`).
2. En sık geçen **üç** kelimeyi, sayılarıyla birlikte yazdır.

```
the 4
and 2
bird 1
```

Sıralama kuralı: sayısı büyük olan önce. **Sayılar eşitse** kelimeler
alfabetik sıraya göre (`bird`, `cat`'ten önce gelir).

İkinci adım işin zor kısmı. `sorted` ile bir kurala göre sıralamak henüz
öğrenmediğin bir şey gerektiriyor; onun yerine "en iyiyi bul" döngüsünü
**üç kez** çalıştır: her turda henüz seçilmemiş kelimeler arasından en
iyisini bul, yazdır ve seçilenlere ekle.

> Dikkat: "En iyi" iki koşullu: daha büyük sayı **ya da** aynı sayı ama
> alfabede daha önce. Metinler de karşılaştırılabilir: `"bird" < "cat"`
> `True`.
