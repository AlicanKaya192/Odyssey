`users` ve `posts` tabloları hazır. `report(user_id)` önce kullanıcının
adını bulsun, sonra o adla yazılmış yazıların başlıklarını (`title`) bir
liste olarak döndürsün; kullanıcı yoksa `[]`. Başlangıç kodu ilk sorguyu
parametreyle yapıyor ama veritabanından okuduğu adı ikinci sorguya
**metinle** ekliyor ve `O'Brien`'da bozuluyor.

**Beklenen çıktı:**

```
['hello']
['notes', 'ideas']
[]
```
