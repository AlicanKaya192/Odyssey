Bir DP tablosunda her hücre yalnızca **son birkaç** hücreye bakıyorsa bütün
tabloyu tutmaya gerek yok.

## Fibonacci: iki değişken

`table[i]` yalnızca `table[i − 1]` ve `table[i − 2]`'ye bakıyor. Tablo yerine
iki değişken yeter: bellek `O(n)`'den `O(1)`'e iner (bir önceki notun
`fib_table`'ı zaten böyleydi).

## Izgara: tek satır

`paths[r][c]` yalnızca üstündeki (`paths[r − 1][c]`) ve solundaki
(`paths[r][c − 1]`) hücreye bakıyor. Tek bir satır tutup soldan sağa
güncellersek, güncellemeden önce hücrede **üstteki satırın** değeri,
solundaki hücrede ise **bu satırın** yeni değeri durur:

```python
def grid_paths_row(rows, cols, blocked):
    row = [0] * cols
    row[0] = 1
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                row[c] = 0
            elif c > 0:
                row[c] += row[c - 1]          # üstten (eski) + soldan (yeni)
    return row[-1]

print(grid_paths_row(3, 3, set()), grid_paths_row(3, 3, {(1, 1)}),
      grid_paths_row(10, 10, set()))
```

```text
6 2 48620
```

Dersteki iki boyutlu tabloyla aynı cevaplar; bellek `rows × cols` yerine
`cols`. Büyük ızgaralarda ya da uzun dizilerde (DP 2'deki düzenleme uzaklığı)
bu fark belleğe sığmakla sığmamak arasındaki fark olabilir.

**Bedeli:** yalnızca cevabı bulursun. Cevabın **nasıl** oluştuğunu (hangi
paralar, hangi yol) geri çıkarmak için tablonun tamamı gerekir.
