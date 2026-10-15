`parse_title(title)` fonksiyonunu yaz. Başlık şu kurala uyuyorsa `[tür, kapsam, uyumsuz, özet]` listesini, uymuyorsa `None` döndürsün:

- Tür: `feat`, `fix`, `docs`, `test` ya da `chore`.
- İsteğe bağlı kapsam parantez içinde, küçük harf ve tire: `(login)`. Yoksa kapsam `None`.
- İsteğe bağlı `!`: varsa uyumsuz `True`, yoksa `False`.
- Sonra `: ` (iki nokta ve boşluk) ve boşlukla başlamayan bir özet.

Düzenli ifadede gruplar `match.groups()` ile alınır; eşleşmeyen isteğe bağlı grup `None` gelir.

**Beklenen çıktı:**

```
['feat', 'login', False, 'remember me']
['fix', None, True, 'drop the old api']
['docs', None, False, 'explain the setup']
None
None
```
