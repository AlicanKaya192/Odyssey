Çalışan bir betik ile güvenilir bir betik arasındaki fark birkaç alışkanlıktır.

## Önce terminalde dene

Betik, terminalde çalıştığını gördüğün komutların kaydıdır. Her komutu önce
tek başına çalıştır, sonra dosyaya koy.

## Argümanları denetle

Betiğin başında beklediğin argümanların gelip gelmediğine bak; gelmediyse ne
yazılması gerektiğini söyleyip `exit 1` ile çık:

```bash
if [ $# -lt 1 ]; then
  echo "usage: backup.sh FILE..."
  exit 1
fi
```

## Değişkeni hep tırnakla kullan

`cp $f $f.bak` adı `my notes.txt` olan bir dosyada dört ayrı kelimeye bölünür.
`cp "$f" "$f.bak"` her zaman doğru çalışır.

## Hata olunca dur

bash bir komut düşse de sonrakine geçer. Gerçek betiklerin başına çoğu zaman şu
satır yazılır:

```bash
set -euo pipefail
```

`-e` bir komut düşünce betiği durdurur, `-u` tanımsız değişkeni hata sayar,
`-o pipefail` borudaki bir düşüşü de yakalar. Bu terminalde `set` yok; gerçek
betiklerinde kullan.

## Adlandır ve açıkla

- Dosya adı ne yaptığını söylesin: `backup.sh`, `x.sh` değil.
- İlk satırların birinde betiğin ne yaptığını ve nasıl çağrıldığını yaz.
- Kendi değişkenlerine küçük harfli ad ver; büyük harfliler ortamın.

## Ne zaman betik değil

Betik birkaç komutu birleştirmek için harikadır. Hesap, veri yapısı ya da
yüzlerce satır gerekiyorsa Python daha okunur ve daha az tuzaklıdır.
