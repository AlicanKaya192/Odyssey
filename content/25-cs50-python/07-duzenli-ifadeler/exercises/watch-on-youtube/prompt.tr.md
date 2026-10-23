Web sayfaları YouTube videolarını bir `iframe` ile gömer:

`<iframe width="560" height="315" src="https://www.youtube.com/embed/xvFZjo5PgG0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>`

Bu adresin kısa hâli `https://youtu.be/xvFZjo5PgG0`. `watch.py`'de `parse(s)` yaz: bir HTML metni alır; içinde bir `iframe`'in `src` özelliğinde YouTube gömme adresi varsa kısa adresi metin olarak döndürür, yoksa `None`. Adres şu biçimlerden biri: `http://youtube.com/embed/...`, `https://youtube.com/embed/...`, `https://www.youtube.com/embed/...` (`http://www.` da olabilir). `src`'nin değeri çift tırnak içinde; `iframe`'in başka özellikleri de olabilir; metinde en fazla bir adres var. `main` HTML'i sorar ve `parse`'ın sonucunu yazar.

## Nasıl denenir

- Girdi `<iframe src="http://www.youtube.com/embed/xvFZjo5PgG0"></iframe>` → çıktı `https://youtu.be/xvFZjo5PgG0`
- Girdi `<iframe width="560" height="315" src="https://www.youtube.com/embed/xvFZjo5PgG0" title="YouTube video player" frameborder="0" allowfullscreen></iframe>` → çıktı `https://youtu.be/xvFZjo5PgG0`
- Girdi `<iframe src="https://cs50.harvard.edu/python"></iframe>` → çıktı `None`
