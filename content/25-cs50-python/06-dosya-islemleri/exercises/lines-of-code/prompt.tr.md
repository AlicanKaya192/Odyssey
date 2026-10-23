Bir programın kaç satır koddan oluştuğunu bilmek ilginç olabilir; yorumlar ve boş satırlar sayılmaz.

Komut satırından **tam bir** argüman (bir Python dosyasının adı ya da yolu) bekleyen ve o dosyadaki kod satırlarını sayıp yazan bir program yaz. Yorumlar ve boş satırlar hariç: `#` ile başlayan satır (önünde boşluk olabilir) yorumdur; docstring yorum **değildir**, sayılır; yalnızca boşluk içeren satır boştur.

Tam bir argüman yoksa (`Too few command-line arguments` ya da `Too many command-line arguments`), dosyanın adı `.py` ile bitmiyorsa (`Not a Python file`) ya da dosya yoksa (`File does not exist`) `sys.exit` ile çık. (CS50'de dosyanın adı `lines.py`.)

İpucu: `str.lstrip` ve `str.startswith`; `open` `FileNotFoundError` verebilir.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı bir klasörde çalıştırıp çıktını ve yazdığın dosyayı karşılaştırıyor.

- Girdi yok → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py hello.py goodbye.py` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py invalid_extension.txt` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py non_existent_file.py` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py hello.py` → çıktı `2`
- Komut `python cozum.py grade.py` → çıktı `11`
