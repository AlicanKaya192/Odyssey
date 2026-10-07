Gerçek API adreslerini okuma alıştırması. Her birinde kendine şu soruları
sor: hangi bilgisayar, hangi kapı, hangi ek bilgiler?

## Örnek 1

```text
https://api.github.com/repos/python/cpython/issues?state=open&per_page=5
```

- Ana makine `api.github.com`: GitHub'ın API'si (sitesi `github.com`).
- Yol `/repos/python/cpython/issues`: "python" hesabının "cpython" deposunun
  sorun kayıtları. Yolun parçaları bir kaynağa doğru daralıyor.
- Sorgu: yalnızca açık olanlar (`state=open`), sayfada 5 tane
  (`per_page=5`). "Sayfa" fikrini Bölüm 10'da göreceğiz.

## Örnek 2

```text
http://localhost:8000/books/42
```

- `http`, `localhost`, `8000`: kendi bilgisayarında, denediğin bir sunucu.
- Yol `/books/42`: 42 numaralı kitap. Sorgu dizesi yok.

## Örnek 3

```text
https://api.example.com/v2/search?q=fish+%26+chips&lang=en
```

- `v2`: API'nin ikinci sürümü.
- `q` değeri kodlanmış: `+` boşluk, `%26` ise `&`. Çözüldüğünde
  `fish & chips`.

## Yol mu, sorgu mu?

Aynı bilgi iki yere de konabilir: `/books/42` ya da `/books?id=42`. Genel
kural:

- **Tek bir kaynağı** gösteriyorsa **yol**: `/books/42`.
- **Listeyi süzüyor, sıralıyor, sayfalıyorsa** **sorgu**:
  `/books?author=Austen&sort=year`.

Hangisinin kullanılacağına API'yi yazan karar verir; sen belgeye bakarsın.

## Hata avı

Bu adreslerin her birinde bir sorun var:

1. `https://api.example.com/v1weather` → taban ile uç nokta arasında `/`
   eksik.
2. `https://api.example.com/search?q=new york` → boşluk kodlanmamış.
3. `https://api.example.com/search?q=a?lang=en` → ikinci `?` aslında `&`
   olmalı.
4. `https://api.example.com/books#42` → `#` sonrası sunucuya gitmez; kitap
   numarası sunucuya hiç ulaşmaz.
