Satışı çeyreklere topla ve yılın nasıl kapandığına bak.

**Yapman gerekenler:**

1. Dosyayı oku ve çeyreklik toplamları hesapla (`to_period("Q")`).
2. 2024'ün dört çeyreğini `çeyrek toplam` biçiminde alt alta yazdır.
3. 2024'ün dördüncü çeyreğinin birinci çeyreğe göre yüzde kaç yüksek
   olduğunu bir ondalığa yuvarlayıp yazdır.
4. 2024'ün son çeyreğinin 2023'ün son çeyreğine göre yüzde değişimini bir
   ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
2024Q1 26513
2024Q2 24146
2024Q3 26025
2024Q4 30927
16.6
12.0
```

Üçüncü satırdaki artış mevsimsellik (yıl sonu hep yüksek), dördüncü
satırdaki artış trend (aynı çeyrek, bir yıl sonra). İkisini ayırmanın yolu
**aynı dönemi** karşılaştırmak.
