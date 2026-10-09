`Exception`'dan türeyen `InsufficientFunds` adında bir hata sınıfı yaz.
Sonra `Wallet` sınıfının `spend(amount)` metodunu düzelt:

- `amount` 0 ya da daha küçükse `ValueError("amount must be positive")`
  fırlatsın.
- `amount` bakiyeden büyükse
  `InsufficientFunds(f"balance {self.balance}, wanted {amount}")` fırlatsın.
- İkisi de değilse tutarı bakiyeden düşsün.

Hata fırlatılınca bakiye **değişmemeli**. Alttaki kod üç harcamayı deniyor;
beklenen çıktı:

```
spent 20
ValueError: amount must be positive
InsufficientFunds: balance 30, wanted 100
30
```
