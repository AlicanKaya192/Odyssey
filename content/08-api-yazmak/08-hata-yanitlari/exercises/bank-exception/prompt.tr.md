`accounts` sözlüğü hazır: `ada` 100, `alan` 20.

**Yapman gerekenler:**

1. `InsufficientFunds` adında, `balance` alanı olan bir istisna sınıfı.
2. `withdraw(name, amount)` yardımcısı: bakiye yetmezse
   `InsufficientFunds(bakiye)` fırlatsın; yetiyorsa düşüp yeni bakiyeyi
   döndürsün. **HTTP bilmesin.**
3. Bu istisnayı `400`, `{"error": "insufficient_funds", "balance": ...}`
   cevabına çeviren yakalayıcı.
4. `POST /accounts/{name}/withdraw?amount=...` → `{"name": ..., "balance": ...}`

- `POST /accounts/ada/withdraw?amount=30` → `{"name": "ada", "balance": 70}`
- `POST /accounts/alan/withdraw?amount=50` → `400`, `{"error": "insufficient_funds", "balance": 20}`
