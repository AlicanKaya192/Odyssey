Bir oy listesi verilmiş:

```python
votes = ["python", "go", "python", "rust", "go", "python"]
```

Her seçeneğin **kaç oy aldığını** say ve `counts` adında bir sözlükte tut.
Sonra sözlüğü yazdır. Beklenen çıktı:

```
{'python': 3, 'go': 2, 'rust': 1}
```

Yöntem şu: boş bir sözlükle başla, liste üzerinde dön, her oy için sözlükteki
sayıyı bir artır. Anahtar henüz yoksa sıfırdan başlaman gerekiyor.

> Sözlükteki çiftlerin sırası, **ilk eklenme sırasıdır**. Listede önce
> `python`, sonra `go`, sonra `rust` geçtiği için çıktı da bu sırada olacak.
