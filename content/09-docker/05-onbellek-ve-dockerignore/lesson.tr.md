# Derleme Önbelleği ve .dockerignore

İlk `docker build` biraz sürüyor; kodda küçük bir değişiklik yapıp yeniden
kurduğunda ise derleme bir saniyede bitiyor. Bunun sebebi **derleme
önbelleği** (build cache). Önbelleği anlamak, Dockerfile'ı neden belli bir
sırayla yazdığımızın cevabı. Bu bölümde bir de imaja **girmemesi gereken**
dosyaları dışarıda bırakmayı öğreneceğiz.

## Önbellek nasıl çalışıyor?

Docker her talimatı çalıştırmadan önce şunu soruyor: **"Bu adımı daha önce
tam olarak aynı hâliyle yaptım mı?"**

- Talimatın metni aynı mı?
- Bir önceki adım aynı mı?
- `COPY` ise kopyalanan dosyaların **içeriği** aynı mı?

Cevap evetse adımı yeniden çalıştırmıyor; geçen seferki katmanı alıyor ve
çıktıya `CACHED` yazıyor. Hayırsa adımı çalıştırıyor.

Kritik kural: **bir adım değişince ondan sonraki bütün adımlar da yeniden
çalışıyor.** Katmanlar üst üste dizili; alttaki değişince üsttekiler de
geçersiz.

<figure class="fig">
  <div class="flow">
    <span class="node ok">FROM<br><small>CACHED</small></span><span class="arrow">→</span>
    <span class="node ok">WORKDIR<br><small>CACHED</small></span><span class="arrow">→</span>
    <span class="node no">COPY . .<br><small>değişti</small></span><span class="arrow">→</span>
    <span class="node no">RUN pip install<br><small>yeniden</small></span><span class="arrow">→</span>
    <span class="node no">CMD<br><small>yeniden</small></span>
  </div>
  <figcaption>Zincirin bir halkası değişince ondan sonraki her adım yeniden çalışıyor. Pahalı adımları değişen adımların <b>önüne</b> koy.</figcaption>
</figure>

## Doğru sıra: kod değişince ne oluyor?

Bir önceki bölümün iskeleti:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

`app.py`'de bir satır değiştirip yeniden kurduğunda (çıktı kısaltıldı):

```text
#7 [2/5] WORKDIR /app
#7 CACHED
#6 [3/5] COPY requirements.txt .
#6 CACHED
#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED
#9 [5/5] COPY . .
#9 DONE 0.0s
```

`requirements.txt` değişmediği için pip adımı **önbellekten** geldi; yalnızca
son `COPY` yeniden çalıştı. (Adımlar paralel hazırlandığı için çıktıdaki
sıra biraz karışık; köşeli parantezdeki numaraya bak.)

## Yanlış sıra: aynı değişiklik

Şimdi kısa yolu deneyelim: her şeyi tek seferde kopyala, sonra kur.

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

`app.py`'de aynı küçük değişiklik:

```text
#6 [2/4] WORKDIR /app
#6 CACHED
#7 [3/4] COPY . .
#7 DONE 0.0s
#8 [4/4] RUN pip install --no-cache-dir -r requirements.txt
#8 DONE 1.2s
```

`COPY . .` `app.py`'yi de kopyaladığı için değişti; ondan sonraki pip adımı
da **yeniden** çalıştı. Burada 1,2 saniye, çünkü listede paket yok. Gerçek
bir projede pandas, scikit-learn ve onlarca paket var; her kod değişikliğinde
**dakikalarca** yeniden kurulum.

## Kural: az değişen önce, çok değişen sonra

Dockerfile'ı **en az değişenden en çok değişene** doğru yaz:

1. Taban imaj (yılda birkaç kez değişir)
2. Sistem paketleri
3. `requirements.txt` ve `pip install` (ayda birkaç kez)
4. Kodun kendisi (günde onlarca kez)

İki ayrı `COPY`'nin sebebi buydu: önce yalnızca bağımlılık listesi, sonra
kod.

## `RUN`'ın önbelleği metne bakıyor

`RUN` adımının önbelleği yalnızca **komutun metnine** (ve önceki adımlara)
bakıyor; dış dünyada ne değiştiğini bilmiyor. Bu iki yerde şaşırtıyor:

```dockerfile
RUN apt-get update
RUN apt-get install -y curl
```

İlk satır bir kez çalışıp önbelleğe girdi. Aylar sonra ikinci satıra yeni bir
paket eklediğinde birinci satır yine önbellekten geliyor; paket listesi
aylar öncesinin listesi ve kurulum düşebiliyor. Çözüm: ikisini **tek
`RUN`'da** birleştirmek.

```dockerfile
RUN apt-get update && apt-get install -y curl
```

Önbelleği tamamen yok saymak gerekirse:

```text
docker build --no-cache -t greeter .
```

## Derleme bağlamı ve `.dockerignore`

`docker build .` başlarken klasörün **tamamını** motora gönderiyor:

```text
#5 transferring context: 5.00MB 0.3s done
```

Klasörde 5 MB'lık bir veri dosyası ve `.git` klasörü vardı. Hepsi
gönderildi ve `COPY . .` ile imaja da girdi. Büyük projelerde bu yüzlerce
MB oluyor.

Daha kötüsü: klasördeki **`.env`** dosyası (şifreler, API anahtarları)
imajın içine giriyor. İmajı paylaşan herkes onu da paylaşmış oluyor.

Çözüm, Dockerfile'ın yanına **`.dockerignore`** adlı bir dosya koymak.
İçindeki kalıplara uyan dosyalar bağlama hiç girmiyor:

```text
# Python (her klasörde)
**/__pycache__
**/*.pyc
.venv

# Git
.git

# Gizli ayarlar
.env

# Büyük veri
data/
```

Aynı klasörde yeniden:

```text
#5 transferring context: 140B done
```

5 MB'tan 140 bayta. `COPY . .` artık bu dosyaları göremiyor.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>.dockerignore yok</h4><p>app.py, requirements.txt</p><p>.git/ (geçmiş)</p><p>.env (şifreler!)</p><p>data/ (5 MB)</p><p><b>bağlam: 5.00 MB</b></p></div>
    <div class="ok"><h4>.dockerignore var</h4><p>app.py, requirements.txt</p><p><b>bağlam: 140 B</b></p><p>sır yok, veri yok</p></div>
  </div>
  <figcaption>Bağlama girmeyen dosya <code>COPY . .</code> ile imaja da giremez.</figcaption>
</figure>

## `.dockerignore` kalıpları

| Kalıp | Ne dışarıda kalır? |
|---|---|
| `.env` | Kökteki `.env` dosyası |
| `*.pyc` | Kökteki bütün `.pyc` dosyaları |
| `**/*.pyc` | Her klasördeki `.pyc` dosyaları |
| `**/__pycache__` | Her klasördeki `__pycache__` |
| `data/` ya da `data` | Kökteki `data` klasörü ve içindekiler |
| `!data/sample.csv` | Bir önceki kuralın **istisnası**: bu dosya girer |
| `# ...` | Yorum |

Kalıplar derleme bağlamının köküne göre okunuyor. `__pycache__` yalnızca
kökteki klasörü dışarıda bırakıyor; `app/__pycache__` için `**/` gerekiyor.

Bir faydası daha var: dışarıda bırakılan bir dosya değişince `COPY . .`
önbelleği **bozulmuyor**. Örneğin `notes.md`'yi `.dockerignore`'a yazarsan
notunu düzenlemek derlemeyi yeniden başlatmaz.

## Özet

- Docker her adımda "aynısını daha önce yaptım mı?" diye soruyor; evetse
  `CACHED`.
- **Bir adım değişince sonraki bütün adımlar yeniden çalışır.**
- Az değişeni önce, çok değişeni sonra yaz: önce `requirements.txt` +
  `pip install`, sonra `COPY . .`.
- `RUN` önbelleği metne bakar; `apt-get update` ile `install`'u tek
  `RUN`'da birleştir. `--no-cache` önbelleği yok sayar.
- `.dockerignore` bağlama girmeyecekleri belirler: `.git`, `.venv`,
  `__pycache__`, `.env`, büyük veri. İmaj küçülür, sırlar sızmaz, önbellek
  gereksiz yere bozulmaz.
