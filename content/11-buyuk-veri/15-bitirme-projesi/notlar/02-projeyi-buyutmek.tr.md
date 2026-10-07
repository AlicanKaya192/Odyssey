Bu projeyi kendi verinle ya da daha büyük bir ölçekte tekrar etmek için
fikirler.

## Kendi verinle

- Açık veri setleri: belediyelerin, ulaşım kurumlarının yayımladığı yolculuk
  ya da sensör verileri çoğu zaman milyonlarca satırlık CSV'ler. Aynı hattı
  uygula: ölç, küçült, Parquet'e çevir, bölümle, sorgula, doğrula.
- Önce hangi soruları soracağını yaz. Bölümleme sütunu sorulardan çıkar.

## Daha büyük ölçek

| Değişen | Hatta ne olur |
|---|---|
| Veri belleğin birkaç katı | Çevirme parça parça kalır; sorgular DuckDB ile |
| Veri diskin sınırında | Sütun seç, sıkıştır, eski bölümleri arşivle |
| Veri tek makineyi aşıyor | Aynı adımlar dask ya da Spark ile |
| Her gün yeni veri | Yalnızca yeni günün bölümünü ekle, eskileri yeniden yazma |
| Canlı veri | Kafka + pencereler; gün sonunda göle yaz |

## Her gün yeni veri: artımlı yükleme

Projede her gece bütün yılı yeniden çevirdik. Gerçek bir hatta yalnızca
**yeni** gün işlenir ve göle yeni bir dosya olarak eklenir:

```python
new_day.to_parquet("lake/month=2024-12/part-31.parquet", index=False)
```

DuckDB `lake/*/*.parquet` kalıbıyla yeni dosyayı kendiliğinden görür. Eski
dosyalara dokunulmaz; bu hem hızlı hem güvenli (yarıda kalan bir yazma eski
veriyi bozmaz).

## Tekrar çalıştırılabilir hat

- Her adım aynı girdiyle aynı çıktıyı versin; adımı ikinci kez çalıştırmak
  zarar vermesin (Bölüm 14'teki etkisiz tekrar).
- Ara dosyaları adımın adıyla sakla; bir adım düşerse baştan değil oradan
  devam et.
- Her adımdan sonra satır sayısını yazdır; sayı beklenmedik değiştiyse dur.

## Buradan sonra öğrenilebilecekler

- **Bulut depolama:** S3 gibi bir depodaki Parquet dosyalarını DuckDB ile
  okumak.
- **Tablo biçimleri:** Delta Lake, Apache Iceberg: Parquet göllerine
  güncelleme, silme ve sürüm ekliyor.
- **İş akışı araçları:** Airflow gibi araçlar hattın adımlarını her gece
  sırayla çalıştırıyor ve düşeni haber veriyor.
