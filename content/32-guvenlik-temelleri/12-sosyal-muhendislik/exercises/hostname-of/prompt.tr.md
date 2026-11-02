`hostname_of(url)` bir adresin gittiği sunucunun adını küçük harflerle
döndürmeli; bulunamazsa boş metin.

Başlangıç kodu adresi `/` işaretinden bölüyor. `school.example@evil.test`
gibi kullanıcı adı içeren ya da `:8443` gibi port içeren adreslerde yanlış
sonuç veriyor. `urllib.parse.urlsplit(url).hostname` kullan; o hem
kullanıcı adını hem portu ayırır, adı da küçük harfe çevirir.

**Beklenen çıktı:**

```
login.school.example
evil.test
files.example
login.school.example
```
