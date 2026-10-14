| Yazılan | Sonuç | Doğrusu |
|---|---|---|
| `python-version: 3.10` | Sayı olarak okunur, `3.1` olur | `python-version: "3.10"` |
| Girintide sekme (Tab) | Okuyucu durur: sekme karakteri bir şey başlatamaz | Yalnızca boşluk |
| `with:` adımın `-` işaretiyle aynı hizada | Okuyucu durur; `with` adımın parçası sayılmaz | `with:`, `uses:` ile aynı hizada |
| `runs-on:ubuntu-latest` | İki noktadan sonra boşluk yok: anahtar sayılmaz | `runs-on: ubuntu-latest` |
| Adımlar `-` olmadan | Liste değil, sözlük olur | Her adım `- ` ile başlar |
| `run: echo a: b` | İkinci iki nokta yeni bir anahtar sanılabilir | Komutu tırnakla ya da <code>run: &#124;</code> ile yaz |

**Girintiyi okumak**

```yaml
jobs:            # 0 boşluk
  test:          # 2 boşluk: jobs'un içinde
    runs-on: x   # 4 boşluk: test'in içinde
    steps:       # 4 boşluk: test'in içinde
      - uses: y  # 6 boşluk: steps listesinin elemanı
        with:    # 8 boşluk: aynı adımın parçası
          k: v   # 10 boşluk: with'in içinde
```

Bir anahtarın neye ait olduğunu bulmak için yukarı doğru, kendisinden
**daha az** girintili ilk satıra bak.

**Okuyucunun mesajı ne diyor?**

- `found character '\t'`: bir yerde sekme var.
- `expected <block end>` ya da `mapping values are not allowed here`:
  girinti kaymış ya da iki noktadan sonra boşluk yok.
- Mesajdaki satır numarası sorunun **bulunduğu** satırdır; asıl hata çoğu
  zaman bir iki satır yukarıdadır.
