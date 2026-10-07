Büyük veri yazılarında, ders slaytlarında ve iş ilanlarında sık geçen
kelimeler. Her birinin patikada nerede ayrıntılı anlatıldığı yanında.

## Donanım

| Terim | Anlamı |
|---|---|
| **Bellek (RAM)** | Programın o anda çalıştığı, hızlı ama küçük ve geçici alan. |
| **Disk (SSD, HDD)** | Dosyaların kalıcı durduğu, büyük ama bellekten yavaş alan. |
| **Sayfa dosyası** (*swap*) | Bellek dolunca işletim sisteminin diske taşıdığı kısım. Program çökmez ama çok yavaşlar. |
| **Çekirdek** (*core*) | İşlemcinin aynı anda iş yapabilen birimlerinden biri. 8 çekirdek, 8 iş aynı anda (Bölüm 10). |
| **Düğüm** (*node*) | Bir kümedeki tek bir bilgisayar. |
| **Küme** (*cluster*) | Bir iş için birlikte çalışan bilgisayarlar (Bölüm 12–13). |

## Kavramlar

| Terim | Anlamı |
|---|---|
| **Bellek dışı** (*out-of-core*) | Belleğe sığmayan veriyi parça parça işlemek (Bölüm 3). |
| **Dikey ölçekleme** (*scale up*) | Daha güçlü tek makine. |
| **Yatay ölçekleme** (*scale out*) | Daha çok makine. |
| **Dağıtık işleme** | İşi birden çok makineye bölmek (Bölüm 12–13). |
| **Toplu işleme** (*batch*) | Biriken veriyi belli aralıklarla, topluca işlemek. |
| **Akan veri** (*streaming*) | Veriyi geldiği anda işlemek (Bölüm 14). |
| **Sütunlu biçim** | Veriyi satır satır değil sütun sütun saklayan dosya biçimi; Parquet (Bölüm 4–5). |
| **Bölümleme** (*partitioning*) | Veriyi bir sütuna göre ayrı dosyalara ayırmak (Bölüm 6). |
| **Örnekleme** (*sampling*) | Verinin tamamı yerine temsil eden bir parçasıyla çalışmak (Bölüm 9). |

## Büyük verinin V'leri

| V | Soru | Örnek |
|---|---|---|
| **Volume** (hacim) | Ne kadar? | 5 yıllık bütün siparişler, 2 TB |
| **Velocity** (hız) | Ne kadar hızlı geliyor? | Saniyede 10 000 tıklama |
| **Variety** (çeşitlilik) | Hangi biçimde? | Tablo + JSON + resim + metin |
| **Veracity** (doğruluk) | Ne kadar güvenilir? | Bozuk sensör ölçümleri |
| **Value** (değer) | İşe yarıyor mu? | Hangi ürün birlikte alınıyor? |

## Araçlar

| Araç | Ne işe yarar | Patikada |
|---|---|---|
| **pandas** | Belleğe sığan tabloyla çalışmak | Her bölümde |
| **pyarrow** | Parquet okuyup yazmak, sütunlu bellek | Bölüm 4–6 |
| **DuckDB** | Dosyanın üstünde SQL, tek makinede | Bölüm 7–8 |
| **dask** | pandas'a benzeyen, parça parça ve paralel tablo | Bölüm 11 |
| **Hadoop** | Dağıtık depolama (HDFS) ve MapReduce | Bölüm 12 |
| **Spark** | Kümede bellek içi dağıtık işleme | Bölüm 13 |
| **Kafka** | Akan veriyi taşıyan mesaj sistemi | Bölüm 14 |
