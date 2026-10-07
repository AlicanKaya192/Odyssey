Bu patikadan sonra öğrenmeye devam etmek için yollar.

## Odyssey'de sıradakiler

- **Veri Mühendisi rotası:** Büyük Veri'den sonra API patikaları (bir veri
  hattının sonucunu servis olarak sunmak) ve Docker (hattı her bilgisayarda
  aynı çalışacak şekilde paketlemek).
- **Zaman Serileri:** akan verinin pencereleri ve olay zamanı, zaman
  serilerinde tahmin yaparken de karşına çıkıyor.
- **Makine Öğrenmesi:** büyük bir veriden modele girecek örneği seçerken
  ölçmek, örneklemek ve doğrulamak aynen geçerli.

## Gerçek araçları kendi bilgisayarında denemek

| Araç | Nasıl başlanır |
|---|---|
| PySpark | Java (JDK 17 gibi) kur, `pip install pyspark`, `local[*]` ile tek makinede |
| Kafka | Docker ile tek konteynerde çalışan bir Kafka imajı |
| Polars | `pip install polars`: pandas'a benzeyen, sütunlu ve paralel bir tablo kütüphanesi |
| DuckDB | Zaten biliyorsun: komut satırı aracı da var (`duckdb`) |

Bölüm 13'teki `minispark` kodunu `from pyspark.sql import SparkSession` ile
gerçek Spark'ta çalıştırmak iyi bir ilk adım; farklar Spark Kartı notunda.

## Buradan sonra öğrenilebilecek konular

- **Bulut depolama:** Amazon S3, Google Cloud Storage. Parquet gölleri
  çoğunlukla orada duruyor; DuckDB ve Spark oradaki dosyaları okuyabiliyor.
- **Tablo biçimleri:** Delta Lake, Apache Iceberg. Parquet göllerine
  güncelleme, silme, sürüm (geçmişe dönme) ekliyorlar.
- **İş akışı araçları:** Apache Airflow, Dagster. Hattın adımlarını her
  gece sırayla çalıştırıyor, düşeni haber veriyor, yeniden deniyorlar.
- **Veri ambarları:** BigQuery, Snowflake. Sunucusu başkasında duran,
  terabaytlarda SQL çalıştıran servisler (ücretli).
- **Akış işleme:** Apache Flink, Spark Structured Streaming; Bölüm 14'teki
  pencereler ve su işaretleri orada hazır.

## Kendi projen

1. Milyonlarca satırlık açık bir veri seti bul (ulaşım, hava durumu, enerji
   tüketimi).
2. Önce ne soracağını yaz.
3. Bitirme projesindeki hattı uygula: ölç, küçült, Parquet'e çevir,
   bölümle, DuckDB ile sorgula, iki yoldan doğrula.
4. Her adımda ölçtüğün sayıyı not et; sonunda "ne kazandım" sorusuna sayıyla
   cevap ver.
