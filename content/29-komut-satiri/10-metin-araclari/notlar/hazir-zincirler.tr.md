Gerçek işlerde tekrar tekrar yazılan zincirler. Dosya adlarını kendi
dosyanla değiştir.

## Hangisi kaç kez?

```bash
cut -d ' ' -f 2 visits.log | sort | uniq -c | sort -rn
```

Kes, sırala, say, sayıya göre sırala. İlk beşi için sona `| head -n 5`.

## En sık geçen kelimeler

```bash
tr ' ' '\n' < metin.txt | sort | uniq -c | sort -rn | head -n 10
```

Büyük/küçük harf ayrımı olmasın istersen başa `tr A-Z a-z` ekle.

## Bir sütunun tekrarsız değerleri

```bash
tail -n +2 sales.csv | cut -d , -f 2 | sort -u
```

`tail -n +2` başlık satırını atar.

## En büyük N satır

```bash
sort -t , -k 3 -rn sales.csv | head -n 3
```

## Hata türleri

```bash
grep -i error app.log | cut -d ' ' -f 4- | sort | uniq -c
```

Önce süz, sonra hatanın metnini kes ve say.

## Tekrar eden satırlar

```bash
sort names.txt | uniq -d
```

Bir listede iki kez yazılmış olanları bulur.

## Dağınık boşlukları düzelt

```bash
tr -s ' ' < messy.txt > clean.txt
```

Sonucu her zaman **başka** bir dosyaya yaz; `> messy.txt` dosyayı okumadan
önce boşaltır.
