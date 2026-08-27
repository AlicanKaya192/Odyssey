Bu uygulamayı kullanmak için bilgisayarına Python kurmana gerek yok — alıştırmalar uygulamanın içinde çalışıyor. Ama er ya da geç kendi projelerini yazmak isteyeceksin, o zaman kurulum gerekiyor.

## Windows'a kurmak

[python.org/downloads](https://www.python.org/downloads/) adresinden kurulum dosyasını indir.

Kurulum ekranında **çok önemli bir kutu** var:

> ☑ **Add python.exe to PATH**

Bunu işaretlemeden devam edersen komut satırında `python` yazdığında "böyle bir komut yok" hatası alırsın. Sonradan düzeltmek mümkün ama uğraştırıcı; ilk seferde işaretle.

## Kurulumu doğrulamak

Komut satırını (Windows'ta `cmd` veya PowerShell) açıp şunu yaz:

```
python --version
```

Bir sürüm numarası görüyorsan kurulum tamam.

## Hangi sürüm?

En güncel sürümü kur. İnternette bulacağın eski örnekler bazen Python 2 ile yazılmış olabilir; en belirgin farkı `print` kullanımıdır:

```python
print "merhaba"      # Python 2 — artık çalışmaz
print("merhaba")     # Python 3 — doğru kullanım
```

Bir örnek çalışmıyorsa önce bunu kontrol et.

## Anaconda'ya dikkat

Veri bilimi kaynaklarında sık sık **Anaconda** kurulumu önerilir. Anaconda, Python'la birlikte NumPy ve pandas gibi kütüphaneleri de getirdiği için pratiktir.

Ancak bilmen gereken bir şey var: Anaconda kendi sistem kütüphanelerini taşır ve bunlar bazı programlarla çakışabilir. Bu uygulamanın kendisi de Anaconda'nın Python'uyla kurulduğunda açılmıyor — arayüz kütüphanesi Anaconda'nın eski dosyalarını yükleyip hata veriyor.

Yeni başlıyorsan **temiz bir Python kurulumuyla** başlamanı öneririm. Kütüphaneleri ihtiyaç duydukça `pip install` ile eklersin.

## Bir düzenleyici seç

Kodu Not Defteri'nde de yazabilirsin ama işini zorlaştırırsın. Yaygın seçenekler:

- **VS Code** — ücretsiz, hafif, en çok kullanılan
- **PyCharm** — Python'a özel, topluluk sürümü ücretsiz
- **Jupyter Notebook** — veri analizinde çok kullanılır; kodu parça parça çalıştırıp sonucu hemen görürsün

Veri bilimiyle ilgileniyorsan Jupyter'i erken tanımanda fayda var.
