İzinlerin arkasındaki kullanıcı düzeni ve gerçek bir Linux'ta yönetici olarak
çalışmak. Bu terminalde `sudo` ve kullanıcı değiştirme yok; burada yazanlar
gerçek bir sistemde işine yarayacak.

## Kullanıcılar ve gruplar

- Her dosyanın bir **sahibi** ve bir **grubu** vardır (`ls -l`'deki iki ad).
- Her kullanıcının bir numarası (*uid*) vardır; `id` gösterir.
- Bir kullanıcı birden çok grupta olabilir. Ekip bir grupta toplanır, ortak
  dosyaların grubu o grup yapılır ve `g+w` verilir.
- Kullanıcıların listesi `/etc/passwd` dosyasındadır; şifreler orada değil,
  yalnızca root'un okuyabildiği ayrı bir dosyadadır.

## root

**root** (uid 0) sistemin yöneticisidir; izinler onu durdurmaz. Bu yüzden
root olarak günlük iş yapılmaz: bir yazım hatası bütün sistemi silebilir.

## sudo

Yönetici izni gereken **tek bir** komutun başına `sudo` yazılır:

```bash
sudo apt install tree        # program kurmak
sudo nano /etc/hosts         # bir sistem dosyasını düzenlemek
```

sudo kendi şifreni sorar (root'unkini değil) ve komutu root olarak
çalıştırır. Yalnızca yetki verilmiş kullanıcılar kullanabilir.

Kurallar:

- Bir komut `Permission denied` verdi diye hemen `sudo` ekleme. Önce sor:
  bu dosyayı gerçekten değiştirmem gerekiyor mu, yanlış klasörde miyim?
- İnternetten kopyaladığın `sudo` içeren komutları anlamadan çalıştırma.
- Kendi ev klasöründeki dosyalar için sudo gerekmez. Gerekiyor gibi görünüyorsa
  dosya bir ara root olarak oluşturulmuştur.

## Sahibini değiştirmek

`chown kullanıcı:grup dosya` dosyanın sahibini ve grubunu değiştirir; çoğu
zaman `sudo` ile kullanılır. Bu terminalde yok.

## Git Bash'te izinler

Windows'un dosya sistemi Linux izinlerini tutmaz. Git Bash'te `chmod` çoğu
zaman etkisizdir ve `ls -l` sahip olarak Windows kullanıcını gösterir. İzinler
Linux'ta, bir sunucuda ya da bir Docker konteynerinde önemlidir; bu dersteki
terminal onları Linux'taki gibi davranacak şekilde benzetiyor.
