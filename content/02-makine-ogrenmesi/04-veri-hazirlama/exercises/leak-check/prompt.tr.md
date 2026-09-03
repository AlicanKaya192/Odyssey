Bu bölümdeki örneklerde sızıntının etkisi küçük çıktı. Şimdi büyük
çıktığı yeri göreceksin.

Elinde 80 satır ve 300 sütun var. **Hepsi rastgele sayı** — hedefle
hiçbirinin ilişkisi yok. Doğru kurulan bir model burada hiçbir şey
bulamamalı.

**Yapman gerekenler:**

**Sızıntılı yol:**

1. Her sütunun hedefle olan ilişkisini (mutlak korelasyon) **bütün veriye
   bakarak** hesapla.
2. En yüksek beş sütunu seç.
3. **Sonra** ayır (`random_state=42`), doğrusal regresyon eğit, test
   kümesinde R² hesapla. Üç ondalıkla yazdır.

**Temiz yol:**

4. **Önce** ayır (aynı `random_state`).
5. İlişkileri **yalnızca eğitim** verisinde hesapla ve beş sütunu ona göre
   seç.
6. Aynı modeli eğit, test kümesinde R² hesapla. Üç ondalıkla yazdır.

**Beklenen çıktı:**

```
0.442
-0.273
```

**İkinci sayı doğru olan.** Negatif R², modelin taban çizgiden kötü olduğu
anlamına geliyor — ve burada olması gereken tam olarak bu, çünkü veride
öğrenilecek hiçbir şey yok.

**Birinci sayı uydurma.** 0.442, ortada bir model varmış gibi görünüyor.
Oysa yapılan tek şey sütunları **bütün veriye bakarak** seçmekti.

**Nasıl oluyor:** 300 rastgele sütun arasından bazıları, tesadüfen, test
satırlarındaki hedef değerlerle uyuşuyor. Seçim bütün veriye bakarak
yapıldığında tam olarak o sütunlar seçiliyor — çünkü seçim ölçütü onları
ödüllendiriyor. Sonra model o sütunlarla, o test verisinde ölçülüyor ve
iyi görünüyor.

**Model hiçbir işe yaramaz.** Yeni bir veri geldiğinde o tesadüfi uyum
ortadan kalkıyor.

**Bu sayı bir sunuma konabilir ve kimse fark etmez.** Sızıntının en tehlikeli
tarafı bu: hata mesajı yok, uyarı yok, yalnızca beklenenden güzel bir sayı.

**Pratik kural:** sonuç beklediğinden çok iyiyse önce sevinme, önce sızıntı
ara. R² 0.99 ya da %100 doğruluk, genelde bir başarı değil bir belirti.
