Bir betiğin bütün parçaları, bir bakışta.

## İskelet

```bash
#!/bin/bash
# Ne yaptığını anlatan bir satır.

if [ -z "$1" ]; then
  echo "usage: script.sh FILE"
  exit 1
fi

for f in "$@"; do
  echo "processing $f"
done
```

## Çalıştırmak

| Yazım | Ne gerekir |
|---|---|
| `bash betik.sh` | Okuma izni |
| `./betik.sh` | `chmod +x`, shebang |
| `betik.sh` | Klasörün PATH'te olması |
| `source betik.sh` | Şu anki kabukta çalışır; değişkenleri kalır |

## Özel değişkenler

| Ad | Değer |
|---|---|
| `$0` | Betiğin adı |
| `$1` ... `$9` | Argümanlar |
| `$#` | Argüman sayısı |
| `"$@"` | Bütün argümanlar, ayrı ayrı |
| `$?` | Son komutun çıkış kodu |

## Sınamalar

| Sınama | Anlamı |
|---|---|
| `[ -f yol ]` | Dosya var |
| `[ -d yol ]` | Klasör var |
| `[ -z "$a" ]` | Boş |
| `[ "$a" = "b" ]` | Metin eşit |
| `[ $n -gt 0 ]` | Sayı büyük (`-eq -ne -lt -le -ge`) |

## Döngüler ve fonksiyon

```bash
for i in $(seq 1 3); do echo "$i"; done
while [ $n -gt 0 ]; do n=$((n - 1)); done
greet() { local name=$1; echo "Hi, $name"; }
```
