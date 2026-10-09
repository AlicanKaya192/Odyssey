`notes(argv)` fonksiyonunu yaz: iki alt komutu olan bir ayrıştırıcı kursun
(`add_subparsers(dest="command", required=True)`): `add` bir `text` alır;
`list` `int` türünde `--limit` (varsayılan 10) alır. `add` için
`"added: <text>"`, `list` için `"listing <limit>"` metnini döndürsün.

**Beklenen çıktı:**

```
added: buy milk
listing 3
listing 10
```
