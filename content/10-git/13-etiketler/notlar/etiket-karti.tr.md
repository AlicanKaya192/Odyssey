| Komut | Ne yapar |
|---|---|
| `git tag v1.0` | Bulunduğun commit'e hafif etiket. |
| `git tag -a v1.0 -m "Version 1.0"` | Açıklamalı etiket (sürümler için). |
| `git tag v0.9 <commit>` | Eski bir commit'e etiket. |
| `git tag` / `git tag -l "v1.*"` | Listele / desenle süz. |
| `git tag -n` | Mesajlarıyla listele. |
| `git show v1.0` | Etiket ve commit ayrıntısı. |
| `git tag -d v1.0` | Yerel etiketi sil. |
| `git push origin v1.0` | Bir etiketi GitHub'a gönder. |
| `git push --tags` | Bütün etiketleri gönder. |
| `git push origin --delete v1.0` | GitHub'daki etiketi sil. |
| `git describe` | En yakın açıklamalı etikete göre konum. |
| `git checkout v1.0` | Etiketteki koda bak (HEAD kopuk). |
| `git switch -c fix-1.0 v1.0` | Etiketten dal aç. |
| `git diff v1.0 v1.1` | İki sürüm arasındaki fark. |
| `git log --oneline v1.0..v1.1` | İki sürüm arasındaki commit'ler. |

## Sık hatalar

| Mesaj | Anlamı | Çözüm |
|---|---|---|
| `fatal: tag 'v1.0' already exists` | Aynı adla etiket var. | Başka ad ya da önce `git tag -d`. |
| Etiket GitHub'da görünmüyor | `git push` etiket göndermez. | `git push origin v1.0` |
| `git switch v1.0` hata veriyor | Etiket dal değil. | `git checkout v1.0` ya da `git switch -c dal v1.0` |
| `No annotated tags can describe` | Yalnızca hafif etiket var. | `git describe --tags` |

## `..` ile aralık

`git log v1.0..v1.1` "v1.1'de olup v1.0'da olmayan commit'ler" demek: iki
sürüm arasında ne yapıldı. Sürüm notu yazarken işe yarar.
