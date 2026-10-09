Soyut `Exporter`'dan türeyen `JsonExporter` kurulamıyor: soyut metodu
yanlış adla yazılmış. Metodu doğru adla (`export`) yaz; satırları
`json.dumps(rows)` ile metne çevirsin.

**Beklenen çıktı:**

```
[{"name": "pen", "price": 1.5}]
```
