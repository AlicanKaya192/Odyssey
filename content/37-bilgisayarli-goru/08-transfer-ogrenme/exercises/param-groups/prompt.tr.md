`group_summary(body_lr, head_lr)` hazır `body` ve `head` için iki gruplu bir
`torch.optim.Adam` kursun (gövde `body_lr`, baş `head_lr`) ve her grup için
`[öğrenme oranı, parametre sayısı]` listesini döndürsün
(`optimizer.param_groups`).

**Beklenen çıktı:**

```
[[0.0001, 80], [0.01, 27]]
```
