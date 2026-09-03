Önceki alıştırmada `k`'nın cevabı değiştirdiğini gördün. Şimdi `k`'nın
**neyi** ayarladığını ölçeceksin.

Bölüm 05'ten tanıdık geliyor olmalı: iki skoru birlikte okuyacaksın.

**Yapman gerekenler:**

1. Veriyi hazırla ve ölçekle (önceki alıştırmadaki gibi).
2. Şu `k` değerlerini sırayla dene: **1, 3, 5, 9, 15, 25**.
3. Her `k` için iki doğruluk ölç: **eğitim** kümesinde ve **test**
   kümesinde.
4. Her `k` için tek satır yazdır: **k, eğitim doğruluğu, test doğruluğu** —
   doğruluklar üç ondalık.

**Beklenen çıktı:**

```
1 1.0 0.82
3 0.94 0.86
5 0.94 0.92
9 0.927 0.9
15 0.92 0.88
25 0.927 0.92
```

**Birinci satır: `k=1`'de eğitim doğruluğu 1.000.**

Şaşırtıcı değil, bir an düşününce: her eğitim noktasının kendine **en yakın
komşusu kendisidir**. Uzaklık sıfır. Model o noktanın etiketini kendisinden
okuyor ve hiç yanılmıyor.

Testte ise 0.82'ye düşüyor — bölüm 05'in aşırı öğrenme tablosunun ders
kitabı örneği: **eğitim kusursuz, test zayıf.**

**`k` büyüdükçe** eğitim doğruluğu düşüyor (model artık ezberleyemiyor) ve
test doğruluğu genelde yükseliyor. Ama düzgün bir eğri değil: 0.82 → 0.86 →
0.92 → 0.90 → 0.88 → 0.92, yani zıplıyor.

Bu zıplama tanıdık olmalı — bölüm 05'te de görmüştün ve sebebi aynı: 50
kayıtlık bir test kümesinde tek bir kaydın yer değiştirmesi doğruluğu 0.02
oynatıyor.

**Bu yüzden `k`'yı bu tabloya bakarak seçemezsin.** Nasıl seçileceği bir
sonraki alıştırmada.
