`history_cost(tokens, price_in, price_out)` bir sohbette sırayla gelen
kullanıcı mesajlarının token sayılarını alsın. Her çağrıda o ana kadarki bütün
mesajlar giriş olarak gönderiliyor (cevaplar yok sayılıyor) ve her cevap 20
token. Döndür: `[toplam giren token, toplam maliyet]`; fiyatlar milyon token
başına, maliyet 6 basamağa yuvarlanmış `float` (07).

**Beklenen çıktı:**

```
[94, 0.000167]
```
