Bir sınıfın asıl faydası, nesnenin bir şeyi **hatırlaması**. Bu alıştırmada
çağrılar arasında durumunu koruyan bir nesne yazacaksın.

**Yapman gerekenler:**

1. `Counter` adında bir sınıf yaz.
2. Kurucusu argüman almasın; `count` özelliğini `0` ile başlatsın.
3. `increase` metodu: sayacı bir artırsın ve **yeni değeri** döndürsün.
4. `reset` metodu: sayacı sıfırlasın, bir şey döndürmesin.
5. Bir `Counter` nesnesi kur, üç kez artır, `count` değerini yazdır.
   Sonra sıfırla ve tekrar yazdır.

**Beklenen çıktı:**

```
1
2
3
3
0
```

İlk üç satır `increase` çağrılarının **dönüş değerleri**, dördüncü satır
`count` özelliği, beşinci satır sıfırlandıktan sonraki hâli.

> Sayacı artırmak için `self.count = self.count + 1` yazıyorsun. Metot
> içinde nesnenin verisine her erişimde `self.` gerekiyor.
