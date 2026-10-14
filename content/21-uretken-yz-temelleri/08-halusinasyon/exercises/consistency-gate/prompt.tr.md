Salt okunur `tiny_chat.py` dersteki oyuncak modeli içeriyor. `gate(country, n,
threshold)` soruyu `ask(country, temperature=1.0, seed=s)` ile `s = 0, 1, …,
n-1` için `n` kez sorsun, en sık cevabı ve payını bulsun (eşitlikte abece
sırasında önce gelen). Pay `threshold`'dan küçük değilse cevabı, küçükse
`"I am not sure."` döndürsün.

**Beklenen çıktı:**

```
japan the capital of japan is tokyo .
chile I am not sure.
```
