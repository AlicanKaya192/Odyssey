`find_weak(lines)` kod satırlarından `random` modülünü kullananların
numaralarını (1'den başlayarak) liste olarak döndürsün. Bir satır şu
durumda işaretlenir:

- içinde `random.` geçiyorsa ya da satır (baştaki boşluklar atılınca)
  `from random import` ile başlıyorsa,
- **ama** satır (baştaki boşluklar atılınca) `#` ile başlıyorsa yorumdur,
  işaretlenmez,
- ve `random.SystemRandom` geçiyorsa güvenlidir, işaretlenmez.

Başlangıç kodu `"random" in line` arıyor: `import random`, `os.urandom` ve
yorumları da yakalıyor.

**Beklenen çıktı:**

```
[3, 7]
```
