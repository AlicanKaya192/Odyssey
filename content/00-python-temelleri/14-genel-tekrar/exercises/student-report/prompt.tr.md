Bu alıştırma gerçek bir işin küçük hâli: dosyadan oku, nesneye çevir,
grupla, sırala, raporla.

Yanına `students.txt` konuldu:

```
Ada,90,London
Brian,40,London
Grace,75,NewYork
Alan,60,London
Edith,95,NewYork
```

**Yapman gerekenler:**

1. `Student` sınıfı: kurucusu `name`, `grade`, `city` alsın.
   `is_passing` metodu notu 50 ve üstü ise `True` döndürsün.

2. `load_students` fonksiyonu: dosya adını alsın, `Student` nesnelerinden
   oluşan bir **liste** döndürsün. Boş satırları atlasın.
   Belirtimi: `def load_students(path: str) -> list[Student]:`

3. `students` adlı değişkende yüklenen listeyi tut.

4. `by_city` adlı bir sözlük kur: anahtar şehir, değer o şehirdeki **geçen**
   öğrencilerin adları listesi. Dosyadaki sırayı koru.

5. `best` adlı değişkende en yüksek notu alan öğrencinin **adını** tut.

6. Sırayla şunları yazdır: öğrenci sayısı, `by_city`, `best`.

**Beklenen çıktı:**

```
5
{'London': ['Ada', 'Alan'], 'NewYork': ['Grace', 'Edith']}
Edith
```

> Sözlükte olmayan bir anahtara liste eklerken önce boş liste koyman
> gerekiyor: `if city not in by_city: by_city[city] = []`
