<div align="right">
  <b>Türkçe</b> · <a href="./CONTRIBUTING.md">English</a>
</div>

# Katkıda Bulunma Rehberi

Odyssey'e katkıda bulunmak isteyenler için PR ve issue'lar tamamen açıktır.
Başlamadan önce [Davranış Kuralları](./CODE_OF_CONDUCT.tr.md)'nı okumanı rica ederim.

## 📑 İçindekiler

- [Nasıl katkıda bulunabilirim?](#nasıl-katkıda-bulunabilirim)
- [Geliştirme ortamını kurma](#geliştirme-ortamını-kurma)
- [Hata bildirme](#hata-bildirme)
- [Yeni özellik önerisi](#yeni-özellik-önerisi)
- [İçerik katkısı](#i̇çerik-katkısı)
- [Kod standartları](#kod-standartları)
- [Denetleyicileri çalıştırma](#denetleyicileri-çalıştırma)
- [Pull request süreci](#pull-request-süreci)

## Nasıl katkıda bulunabilirim?

- **Hata düzeltmeleri:** Çalışmayan bir düğme, bozuk bir yerleşim, yanlış bir
  çeviri bulduysan issue aç ya da doğrudan PR gönder.
- **Yeni içerik:** Yeni bir bölüm, alıştırma veya ders notu eklemek istiyorsan
  önce bir issue ile fikrini paylaşman iyi olur. Müfredat sırası
  [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap)
  projesini takip ediyor.
- **Çeviri:** Uygulama Türkçe ve İngilizce. Yeni bir dil eklemek istersen
  `app/i18n/en.json` dosyasını referans al.
- **Dokümantasyon:** README'lerdeki ve kod içindeki açıklamaları iyileştirmek
  her zaman değerlidir.

## Geliştirme ortamını kurma

```bash
py -3.14 tools/setup_env.py
.venv\Scripts\python app\main.py
```

**Anaconda'nın Python'unu kullanma.** Anaconda kendi (eski) MSVC runtime
kütüphanelerini taşıyor; Qt'nin DLL'leri onları yükleyince uygulama
`WinError 127` ile açılmıyor. Temiz bir CPython kurulumu gerekiyor.

## Hata bildirme

Issue açarken şunları yazarsan çok yardımcı olur:

- Ne yapmaya çalıştın, ne bekliyordun, ne oldu
- Adım adım nasıl tekrarlanır
- Windows sürümü ve `python --version` çıktısı
- Varsa ekran görüntüsü ve terminaldeki hata metni

Hazır şablon için [issue şablonlarını](.github/ISSUE_TEMPLATE) kullanabilirsin.

## Yeni özellik önerisi

Öneriyi yazarken "ne eklensin"den çok **hangi sorunu çözdüğünü** anlat. Bir
öğrenci neyi yapamıyor, nerede tıkanıyor? Çözüm fikri varsa ekle ama zorunlu
değil.

## İçerik katkısı

İçerik `content/` altında, JSON ve Markdown olarak duruyor. Uyulması gereken
üç kural var:

### 1. Alıştırma kodu ASCII olmalı

Kullanıcının **yazmak zorunda kaldığı** her şey — değişken adı, fonksiyon adı,
beklenen çıktı, örnek değer — yalnızca ASCII karakter içerir. `ş ğ ı İ ç ö ü`
geçmez.

Sebebi: İngilizce klavyede bu harfler yok. `takim = "Beşiktaş"` isteyen bir
alıştırmayı İngilizce kullanan biri **çözemez**.

```jsonc
// Yanlış
{ "type": "variable", "name": "takim", "equals": "Beşiktaş" }

// Doğru
{ "type": "variable", "name": "team", "equals": "Galatasaray" }
```

Değişken ve fonksiyon adları İngilizce yazılır (`team`, `year`, `total`,
`calculate_age`). Gerçek Python kodu zaten böyle yazılır.

**Ders metni bu kurala girmez** — orası okunur, yazılmaz; Türkçe karakter
serbesttir.

### 2. Bir bölüm iki dili de tamamlanmadan bitmiş sayılmaz

Bir dersin İngilizcesini onu yeni yazmışken hazırlamak fazladan %30-40 zaman
alıyor; aylar sonra yapmaya kalkınca kendi yazdığını baştan okumak gerektiği
için maliyet neredeyse ikiye katlanıyor.

`starter` ve `solution` dosyaları da `{lang}` ile ayrılır, böylece yorum
satırları kullanıcının dilinde olur.

### 3. İçerik id'leri kalıcıdır

Bir bölüme veya alıştırmaya bir kez id verildiyse **asla değiştirilmez**.
Başlık ve dosya adı değişebilir, id sabit kalır — kullanıcıların ilerleme
kayıtları o id'lere bağlı.

## Kod standartları

- Python 3.10+ söz dizimi, tip ipuçlarıyla.
- Renk ve ölçüler `app/resources/theme/tokens.py`'den gelir; widget'lara
  dağınık stil yazılmaz.
- Arayüz metinleri `app/i18n/*.json` içinde; koda sabit metin gömülmez.
- Açıklamalar **neden** olduğunu anlatır, ne olduğunu değil. Kod zaten ne
  olduğunu söylüyor.
- Uygulama içinde yapay zeka veya dış servis çağrısı **yoktur**. Alıştırma
  değerlendirmesi tamamen deterministiktir.

## Denetleyicileri çalıştırma

PR göndermeden önce üçünü de çalıştır:

```bash
.venv\Scripts\python tools\validate_i18n.py      # iki dil eşit mi
.venv\Scripts\python tools\validate_content.py   # şema + ASCII + çeviri kapsamı
.venv\Scripts\python app\main.py                 # uygulama açılıyor mu
```

`validate_content.py` şunları yakalar: eksik dosya, geçersiz sınav cevap
indeksi, dillere göre farklı şık sayısı, çözümün başlangıç koduyla aynı
olması, ASCII ihlalleri ve eksik çeviriler.

## Pull request süreci

1. Depoyu fork'la ve bir dal aç: `git checkout -b duzeltme/kisa-aciklama`
2. Değişikliğini yap, denetleyicileri çalıştır.
3. Commit mesajını açıklayıcı yaz: ne değişti ve **neden**.
4. PR açarken hangi issue'yu kapattığını belirt.

PR'ın kabul edilmesi için:

- Denetleyiciler temiz geçmeli
- Yeni içerik iki dilde olmalı
- Uygulama açılıp ilgili ekran çalışmalı

Küçük yazım düzeltmeleri için issue açmana gerek yok, doğrudan PR gönderebilirsin.
