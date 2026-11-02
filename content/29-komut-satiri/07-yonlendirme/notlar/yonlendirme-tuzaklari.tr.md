Yönlendirmede en sık yapılan hatalar ve nedenleri.

## 1. Okuduğun dosyanın üstüne yazmak

```bash
sort names.txt > names.txt
```

Kabuk önce `names.txt`'yi yazmak için açar ve **boşaltır**, sonra `sort`'u
çalıştırır. `sort` boş bir dosya okur; sonuç boş bir dosya. Doğrusu:

```bash
sort names.txt > sorted.txt
```

## 2. `>` yerine `>>` unutmak

Kayıt dosyasına her seferinde `>` ile yazarsan yalnızca son satır kalır.
Biriktirmek istediğin her dosyada `>>`.

## 3. Hata mesajı dosyaya gitmedi

`komut > out.txt` yalnızca stdout'u yönlendirir. Hata mesajları ekranda
kalır. Hataları da istiyorsan `> out.txt 2>&1`.

## 4. `2>&1` yanlış yerde

| Yazım | Sonuç |
|---|---|
| `komut > f 2>&1` | İkisi de f'ye |
| `komut 2>&1 > f` | Hatalar **ekrana**, çıktı f'ye |

Kabuk yönlendirmeleri soldan sağa uygular. İkinci satırda `2>&1` yazıldığı
anda stdout hâlâ ekrana gidiyordu.

## 5. Hiç yapmadığın bir dosya oluştu

`komut > sonuc.txt` komut başarısız olsa da `sonuc.txt`'yi açar. Boş bir
dosya görürsen önce komutun hata verip vermediğine bak.

## 6. `2>1`

`&` unutulursa `1` bir dosya adı sayılır ve hatalar `1` adında bir dosyaya
yazılır. Doğrusu `2>&1`.
