Derinlik, ağacın karmaşıklık düğmesi. Bölüm 05'ten tanıdık bir tablo
göreceksin — ve bu kez seçimi doğru yapacaksın.

**Yapman gerekenler:**

**Birinci bölüm — derinlik tablosu:**

1. Şu derinlikleri dene: **1, 2, 3, 5, 8, `None`**.
2. Her biri için eğitim ve test doğruluğunu ölç.
3. Tek satır yazdır: **derinlik, eğitim, test**. `None` yerine `none` yaz.

**İkinci bölüm — çapraz doğrulama:**

4. `StratifiedKFold` kur (5 kat, `shuffle=True`, `random_state=42`).
5. Şu derinlikler için **yalnızca eğitim verisinde** çapraz doğrula:
   **1, 2, 3, 5, `None`**.
6. Her biri için tek satır yazdır: **derinlik, CV ortalaması, CV yayılımı**.
7. En yüksek ortalamaya sahip derinliği yazdır.

**Beklenen çıktı:**

```
1 0.807 0.82
2 0.88 0.96
3 0.933 0.8
5 0.993 0.88
8 1.0 0.88
none 1.0 0.88
1 0.753 0.062
2 0.827 0.049
3 0.773 0.057
5 0.813 0.086
none 0.82 0.091
2
```

**Birinci tablodaki eğitim sütununa bak:** 0.807 → 1.000. Sınırsız
derinlikte ağaç her kaydı ayrı bir yaprağa koyup ezberliyor. Bölüm 05'in
aşırı öğrenme tablosunun aynısı.

**Test sütunu ise zıplıyor:** 0.82 → 0.96 → 0.80 → 0.88. 50 kayıtlık bir
test kümesinde tek bir kayıt 0.02 oynatıyor; bu tablo gürültüyle dolu ve
**buradan derinlik seçilmez**.

**İkinci tabloya bak.** En iyi ortalama **derinlik 2**'de (0.827) ve
yayılımı da en küçük (0.049). Fark yayılıma göre anlamlı: ikinci sıradaki
`none` 0.820 ama yayılımı 0.091, yani çok daha kararsız.

**Bu, bölüm 06'nın tersi bir durum.** Orada bütün `k` değerleri gürültü
aralığındaydı ve çapraz doğrulama ayırt edemiyordu; burada rahatça ayırt
ediyor.

**Aynı araç, iki farklı sonuç** — bu yüzden her seferinde yayılıma bakmak
gerekiyor. Ortalama tek başına ne "seçtim" ne de "seçemedim" demeye yetiyor.

Bir güzellik daha: seçtiğin derinlik 2, test kümesinde de en iyi sonucu
veriyor (0.96). Ama bunu **seçimden sonra** öğrendin; test kümesine bakarak
seçseydin ölçüm dürüst olmazdı.
