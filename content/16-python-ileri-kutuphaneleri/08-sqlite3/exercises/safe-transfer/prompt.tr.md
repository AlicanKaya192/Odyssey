`transfer(balances, src, dst, amount)` hesapları kuruyor; senin işin
aktarım: `dst`'ye `amount` ekle, `src`'den çıkar. İki güncelleme **tek
işlemde** (`with conn:`) olsun; `CHECK` kısıtı bozulursa
`sqlite3.IntegrityError`'ı yakala, işlem geri alınsın. Sonda
`dict(conn.execute("SELECT name, balance FROM accounts"))` döndür.

**Beklenen çıktı:**

```
{'ada': 70, 'alan': 50}
{'ada': 100, 'alan': 20}
```
