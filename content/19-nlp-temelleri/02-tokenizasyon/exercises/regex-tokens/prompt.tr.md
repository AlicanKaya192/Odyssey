`tokenize(text)` metni küçük harfe çevirsin ve
`re.findall(r"\w+|[^\w\s]", ...)` ile parçalasın: harf-rakam dizileri ve tek
tek noktalama işaretleri. Başlangıç kodu `split()` kullanıyor; noktalama
kelimelere yapışık kalıyor.

**Beklenen çıktı:**

```
hello|,|world|!|it|'|s|5pm|.
fast|delivery|.|.|.
```
