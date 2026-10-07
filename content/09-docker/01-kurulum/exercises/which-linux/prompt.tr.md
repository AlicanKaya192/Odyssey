Konteynerin kendi dosyaları olduğunu gör. Her Linux'ta `/etc/os-release`
dosyası o sistemin adını ve sürümünü tutuyor; `cat` bir dosyanın içini
ekrana yazan komut.

**Yapman gereken:** `alpine:3.22` imajından başlayan ve çalışınca
`cat /etc/os-release` komutunu çalıştıran bir Dockerfile yaz.

Çıktıda `NAME="Alpine Linux"` satırı görünecek: sen Windows'ta olsan da
konteyner Alpine Linux'un dosyalarını görüyor.
