Pinocchio's Pizza & Subs'ın menüsü CSV olarak hazır: alıştırmanın klasöründe `regular.csv` ve `sicilian.csv`.

Komut satırından **tam bir** argüman (bu biçimde bir CSV dosyasının adı) bekleyen ve dosyayı `tabulate` paketiyle ASCII çizgili bir tablo olarak yazan bir program yaz: `tabulate(..., headers="keys", tablefmt="grid")`. Tam bir argüman yoksa (`Too few command-line arguments` / `Too many command-line arguments`), adı `.csv` ile bitmiyorsa (`Not a CSV file`) ya da dosya yoksa (`File does not exist`) `sys.exit` ile çık. (CS50'de dosyanın adı `pizza.py`; `tabulate` Odyssey'de kurulu.)

İpucu: `csv.DictReader` satırları sözlük olarak verir; `tabulate` sözlüklerin listesini `headers="keys"` ile alır.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı bir klasörde çalıştırıp çıktını ve yazdığın dosyayı karşılaştırıyor.

- Girdi yok → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py regular.csv sicilian.csv` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py non_existent.csv` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py sicilian.txt` → çıktı (boş) (çıkış kodu 1)
- Komut `python cozum.py regular.csv` → çıktı:

```text
+-----------------+---------+---------+
| Regular Pizza   | Small   | Large   |
+=================+=========+=========+
| Cheese          | $13.50  | $18.95  |
+-----------------+---------+---------+
| 1 topping       | $14.75  | $20.95  |
+-----------------+---------+---------+
| 2 toppings      | $15.95  | $22.95  |
+-----------------+---------+---------+
| 3 toppings      | $16.95  | $24.95  |
+-----------------+---------+---------+
| Special         | $18.50  | $26.95  |
+-----------------+---------+---------+
```

- Komut `python cozum.py sicilian.csv` → çıktı:

```text
+------------------+---------+---------+
| Sicilian Pizza   | Small   | Large   |
+==================+=========+=========+
| Cheese           | $25.50  | $39.95  |
+------------------+---------+---------+
| 1 item           | $27.50  | $41.95  |
+------------------+---------+---------+
| 2 items          | $29.50  | $43.95  |
+------------------+---------+---------+
| 3 items          | $31.50  | $45.95  |
+------------------+---------+---------+
| Special          | $33.50  | $47.95  |
+------------------+---------+---------+
```

