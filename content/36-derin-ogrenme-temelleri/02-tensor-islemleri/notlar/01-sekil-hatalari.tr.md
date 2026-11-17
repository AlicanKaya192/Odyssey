Derin öğrenmede en sık görülen hata şekil hatasıdır. Matris çarpımında iç
boyutlar uyuşmazsa PyTorch iki şekli de yazar:

```python
x = torch.ones(4, 3)
w = torch.ones(4, 2)
try:
    x @ w
except RuntimeError as error:
    print(error)
print((x @ w[:3]).shape, (x @ torch.ones(3)).shape)
```

```text
mm: mat1 and mat2 shapes cannot be multiplied (4x3 and 4x2)
torch.Size([4, 2]) torch.Size([4])
```

- `4x3` ile `4x2`: soldakinin sütun sayısı (3) sağdakinin satır sayısına
  (4) eşit değil. Çarpım ancak `(a, b) @ (b, c)` biçiminde olur.
- `w[:3]` ilk üç satırı alıp `(3, 2)` yapıyor; çarpım `(4, 2)`.
- Sağdaki tek boyutlu bir vektörse (`(3,)`) sonuç da tek boyutlu: `(4,)`.

Şekil hatası gördüğünde ilk iş, hatadan hemen önce ilgili tensörlerin
`shape`'ini yazdırmak. Hata Ayıklama bölümünde buna geri döneceğiz.
