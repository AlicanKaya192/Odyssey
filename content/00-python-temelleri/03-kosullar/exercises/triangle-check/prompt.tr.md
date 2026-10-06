Üç kenar uzunluğu verilmiş:

```python
a = 3
b = 4
c = 8
```

Bunlarla bir üçgen kurulabiliyor mu, kurulabiliyorsa ne tür bir üçgen?
Sonucu `kind` değişkenine koy ve yazdır:

- `"not a triangle"`: kurulamıyorsa
- `"equilateral"`: üç kenar eşitse
- `"isosceles"`: tam iki kenar eşitse
- `"scalene"`: hiçbir kenar eşit değilse

```
not a triangle
```

Üçgen kurulabilmesi için **her** iki kenarın toplamı üçüncüden **büyük**
olmalı: `a + b > c`, `a + c > b` ve `b + c > a`. Üçünden biri bile
tutmazsa kenarlar birleşmez.

> Dikkat: Bu kenarların hiçbiri eşit değil, o yüzden aklına ilk
> `"scalene"` gelebilir. Ama önce üçgen kurulup kurulamadığına bakılmalı;
> koşulların **sırası** sonucu değiştiriyor.
