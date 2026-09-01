Gerçek programlarda sınıflar tek başına durmuyor; biri diğerini tutuyor. Bu
alıştırmada **iki sınıf** yazacaksın.

**Yapman gerekenler:**

1. `Student` sınıfı:
   - Kurucusu `name` ve `grade` alsın.
   - `is_passing` metodu: not **50 veya üstü** ise `True` döndürsün.

2. `Course` sınıfı:
   - Kurucusu `title` alsın ve **boş bir** `students` listesi kursun.
   - `enrol` metodu: bir `Student` nesnesi alıp listeye eklesin ve listedeki
     **kişi sayısını** döndürsün.
   - `passing_names` metodu: sınıfı geçen öğrencilerin **adlarını** liste
     olarak döndürsün.

3. Bir `Course` kur (`"Python"`), üç öğrenci ekle:
   `Ada` 90, `Brian` 40, `Grace` 75.
4. Sırayla öğrenci sayısını ve geçen isimleri yazdır.

**Beklenen çıktı:**

```
3
['Ada', 'Grace']
```

Dikkat: `students` listesi **`__init__` içinde** kurulmalı. Sınıf seviyesinde
yazarsan bütün kurslar aynı listeyi paylaşır.

> Listedeki her öğrencinin metodunu çağırabiliyorsun:
> `if student.is_passing():`
