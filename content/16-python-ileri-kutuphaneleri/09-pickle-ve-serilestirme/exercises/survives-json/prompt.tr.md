`survives_json(obj)` fonksiyonunu yaz: `obj`'yi `json.dumps` ile yazıp
`json.loads` ile geri okusun ve sonuç ilkine **eşitse** `True` döndürsün.
JSON yazamazsa (`TypeError`) ya da geri gelen farklıysa (demet listeye,
sayı anahtar metne döner) `False` döndürsün.

**Beklenen çıktı:**

```
True
False
False
False
```
