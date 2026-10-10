`tick(n)` içinde `time.sleep(0.2)` var; `gather` kullanılmasına rağmen dört
iş sırayla gidiyor (0,8 sn). Bekleme satırını olay döngüsünü engellemeyen
hâle getir. Beklenen çıktı:

```
[0, 1, 2, 3] True
```

**Beklenen çıktı:**

```
[0, 1, 2, 3] True
```
