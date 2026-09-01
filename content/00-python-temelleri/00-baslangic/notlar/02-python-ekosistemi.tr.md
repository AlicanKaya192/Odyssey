# Veri Biliminde Python Ekosistemi

Bu bölümde yalnızca `print` yazıyorsun. Ama nereye gittiğini bilmek işe
yarıyor — o yüzden yol haritası burada.

Aşağıdakilerin hiçbirini şimdi öğrenmen gerekmiyor. Adlarını duyduğunda ne
olduklarını bilmen yeterli.

## Neden bu kadar çok kütüphane var?

Python'un kendisi küçük bir dil. Sayı toplar, metin işler, dosya okur.
Veri bilimi işleri — milyonlarca satırı saniyede işlemek, grafik çizmek,
model eğitmek — dilin içinde yok. Bunları **kütüphaneler** yapıyor.

Kütüphane, başkasının yazıp paylaştığı hazır koddur. `import` ile
çağırıyorsun ve kullanmaya başlıyorsun.

## Sıralama

Öğrenme sırası tesadüf değil; her katman altındakine dayanıyor.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Python</b><br>dilin kendisi</span>
    <span class="arrow">→</span>
    <span class="node"><b>NumPy</b><br>sayı dizileri</span>
    <span class="arrow">→</span>
    <span class="node"><b>pandas</b><br>tablolar</span>
    <span class="arrow">→</span>
    <span class="node ok"><b>scikit-learn</b><br>modeller</span>
  </div>
  <figcaption>Her katman bir öncekinin üstüne kuruluyor. pandas içeride NumPy kullanıyor, scikit-learn de ikisini birden.</figcaption>
</figure>

## Ne ne işe yarıyor?

| Kütüphane | Ne yapar | Ne zaman öğreneceksin |
|---|---|---|
| **NumPy** | Sayı dizileri üzerinde hızlı hesap | Veri Bilimi patikası |
| **pandas** | Tablo okuma, süzme, gruplama | Veri Bilimi patikası |
| **Matplotlib** | Grafik çizme | Veri Bilimi patikası |
| **scikit-learn** | Makine öğrenmesi modelleri | Makine Öğrenmesi patikası |
| **SQLite** | Veritabanı (Python'un içinde geliyor) | Python Temelleri sonu |

## Küçük bir önizleme

Bugün bir listedeki sayıların ortalamasını böyle alıyorsun:

```python
scores = [90, 70, 85]
average = sum(scores) / len(scores)
print(average)
```

```
81.66666666666667
```

pandas ile aynı iş, ama bir tablonun tamamı üzerinde:

```python
average = table["score"].mean()
```

Fark hızda değil, **ölçekte.** Üç sayıda ikisi de aynı. Üç milyon satırda
birincisi dakikalar sürüyor, ikincisi saniyeler.

Ama şunu unutma: ikinci satırı yazabilmek için `table["score"]` ifadesinin
ne olduğunu anlaman gerekiyor — o da bu bölümlerde öğreneceğin sözlük ve
liste bilgisi.

## Uygulamada nerede duruyorlar?

Öğrenme yolunda altı patika var:

- **Python** — şu an buradasın. Dilin kendisi.
- **Veri Bilimi** — NumPy, pandas, görselleştirme.
- **Makine Öğrenmesi** — modelleme, özellik mühendisliği.
- **SQL** — veritabanından veri çekme.
- **API** — başka sistemlerden veri alma.
- **Docker** — projeyi her makinede aynı çalıştırma.

Python dışındakiler şimdilik kilitli. Sebebi basit: hepsi Python bilmeyi
gerektiriyor.

## Bir uyarı

Yeni başlayanların en sık yaptığı hata, temelleri atlayıp doğrudan pandas'a
geçmek. İşe yarar gibi görünüyor — çünkü örnekleri kopyalayınca çalışıyor.
Sonra ilk hata mesajında ne yapacağını bilemiyorsun.

Döngü, koşul, fonksiyon ve sözlük bilmeden pandas kullanmak, alfabeyi
bilmeden kitap okumaya benziyor.
