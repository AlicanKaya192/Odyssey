`valid(created, last_seen, now, idle, absolute)` oturum hem boşta kalma
süresini (`now - last_seen < idle`) hem mutlak süreyi (`now - created <
absolute`) aşmadıysa `True`, değilse `False` döndürsün. Başlangıç kodu
yalnızca boşta kalmaya bakıyor.

**Beklenen çıktı:**

```
True
False
False
```
