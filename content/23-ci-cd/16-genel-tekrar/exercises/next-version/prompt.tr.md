`next_version(current, commits)` fonksiyonunu yaz. `current` şu anki sürüm (`"1.4.2"`), `commits` son yayından bu yana gelen commit mesajları.

- Bir mesajın başı (`:`'dan önceki kısım) `!` ile bitiyorsa ya da mesajda `BREAKING CHANGE` geçiyorsa: ANA artar (`2.0.0`).
- Değilse tür `feat` ise (kapsamlı da olabilir: `feat(api)`): YAN artar (`1.5.0`).
- Değilse tür `fix` ise: YAMA artar (`1.4.3`).
- En büyük artış kazanır; artan parçanın sağı sıfırlanır. Hiçbiri yoksa `None`.

**Beklenen çıktı:**

```
1.4.3
1.5.0
2.0.0
None
```
