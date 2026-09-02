Yedi öğrencinin notu elinde. Geçenleri ayıracak ve ortalamalarını
bulacaksın — **döngü ve `if` yazmadan.**

**Yapman gerekenler:**

1. `scores` dizisi başlangıç kodunda hazır.
2. Notu **60 ve üstünde** olanları `passed` adlı diziye al.
3. Notu **60 ile 85 arasında** olanları (60 dâhil, 85 hariç) `middle` adlı
   diziye al.
4. Sırayla yazdır: `passed`, kaç kişi geçtiği, geçenlerin ortalaması
   (iki basamağa yuvarlanmış), `middle`.

**Beklenen çıktı:**

```
[82 91 60 74 88]
5
79.0
[82 60 74]
```

**Tuzak:** iki koşulu birleştirirken `and` **çalışmıyor**, `&` kullanacaksın
ve her koşulu parantez içine alacaksın. `and` yazarsan `ValueError`
alıyorsun.
