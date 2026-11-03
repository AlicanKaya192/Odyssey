Oturum ve Çerez bölümünü uygula. `cookie_problems(header)` bir
`Set-Cookie` değerini `;` ile ayırsın. **İlk parça** çerezin adı ve
değeridir, özellik sayılmaz. Kalan parçaların adlarına (`=`'den önce,
`strip`, küçük harf) bakıp `Secure`, `HttpOnly`, `SameSite`'tan eksik
olanları **bu sırayla** döndürsün.

**Beklenen çıktı:**

```
[]
['Secure', 'SameSite']
['Secure', 'HttpOnly', 'SameSite']
[]
```
