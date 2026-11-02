Ortam değişkenleri bir programa **kodu değiştirmeden** ayar vermenin yoludur.
Öteki patikalarda da karşına çıkanlardan birkaçı:

## Programların okuduğu değişkenler

| Değişken | Kim okur | Ne işe yarar |
|---|---|---|
| `EDITOR` | git ve başka programlar | Hangi düzenleyicinin açılacağı |
| `PATH` | Kabuk | Komutların arandığı klasörler |
| `HOME` | Hemen her program | Ayar dosyalarının yeri |
| `LANG` | Çoğu program | Dil ve karakter kodlaması |
| `LC_ALL=C` | sort ve benzerleri | Her yerde aynı sıralama |
| `PYTHONPATH` | Python | Modüllerin arandığı ek klasörler |

## Sırları koda yazma

Bir API anahtarı ya da veritabanı şifresi kodun içine yazılmaz; kod GitHub'a
gidince sır da gider. Bunun yerine program değeri ortamdan okur:

```bash
export API_KEY=...        # yalnızca kendi terminalinde
python app.py             # program os.environ["API_KEY"] ile okur
```

Python'da `os.environ.get("API_KEY")`, Docker'da `-e` ve `env_file`, GitHub
Actions'ta `secrets` aynı fikrin farklı yazımları. Sırrı `.bashrc`'ye de
yazma; bilgisayarı paylaşıyorsan ya da `.bashrc`'ni yedeklersen o da gider.

## Python sanal ortamı ve PATH

`source .venv/bin/activate` (Windows'ta `.venv\Scripts\activate`) aslında
PATH'in başına `.venv`'in `bin` klasörünü ekler. Bu yüzden ardından yazdığın
`python` sanal ortamın Python'udur. `which python` hangisini kullandığını
gösterir.

## "Kurdum ama bulunamıyor"

1. `which program` boş mu? Program PATH'te değil.
2. Programın kurulduğu klasörü bul.
3. `export PATH="o/klasör:$PATH"` ile dene; çalışıyorsa satırı `.bashrc`'ye
   yaz.
