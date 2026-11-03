Her kopya `[ortam, disarida, saat_once]`. `backup_problems(copies,
rpo_hours)` sorunları bu sırayla döndürsün: `"fewer than 3 copies"`,
`"fewer than 2 media"` (farklı ortam sayısı), `"no offsite copy"`,
`"newest copy too old"` (en yeni kopya `rpo_hours`'tan eski ya da hiç
kopya yok). Yedek ve Felaket Kurtarma.

**Beklenen çıktı:**

```
GOOD
SAME
- fewer than 2 media
BAD
- fewer than 3 copies
- fewer than 2 media
- no offsite copy
- newest copy too old
```
