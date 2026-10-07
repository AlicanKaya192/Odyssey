`git status` çıktısının her parçası ve karşılığı. Takıldığında bu tabloya
bak, sonra Git'in parantez içinde önerdiği komutu oku.

## Uzun çıktının bölümleri

| Başlık | Anlamı | Sıradaki adım |
|---|---|---|
| `On branch main` | Hangi daldasın. | — |
| `No commits yet` | Depoda hiç commit yok. | İlk commit'i at. |
| `Changes to be committed` (yeşil) | Hazırlık alanında, bir sonraki commit'e girecek. | `git commit -m "…"` |
| `Changes not staged for commit` (kırmızı) | İzlenen dosya değişmiş, hazırlık alanında değil. | `git add <dosya>` |
| `Untracked files` (kırmızı) | Git'in hiç izlemediği dosya. | `git add <dosya>` ya da `.gitignore` |
| `nothing to commit, working tree clean` | Her şey commit'te; değişiklik yok. | Çalışmaya devam. |

## Satırların başındaki kelimeler

| Kelime | Anlamı |
|---|---|
| `new file:` | Yeni dosya (hazırlık alanında). |
| `modified:` | İçeriği değişmiş. |
| `deleted:` | Silinmiş. |
| `renamed:` | Adı değişmiş (`git mv` ile). |

## Kısa biçim (`git status -s`)

```text
 M index.html     sağ sütun: değişmiş, hazırlık alanında değil
M  about.html     sol sütun: değişmiş, hazırlık alanında
MM style.css      ikisi birden: eklendi, sonra yine değişti
A  logo.svg       yeni dosya, hazırlık alanında
 D old.html       silinmiş, hazırlık alanında değil
?? notes.txt      izlenmiyor
```

Kural: **sol sütun bir sonraki commit'e girecek olan**, **sağ sütun
girmeyecek olan**.

## Dosyanın dört hâli

| Hâl | Nerede görünür |
|---|---|
| İzlenmeyen (*untracked*) | `Untracked files`, `??` |
| Hazırlanmış (*staged*) | `Changes to be committed`, sol sütun |
| Değiştirilmiş (*modified*) | `Changes not staged…`, sağ sütun |
| Değişmemiş (*unmodified*) | Hiçbir yerde: commit'teki hâliyle aynı |

Değişmemiş dosyalar `git status`'ta görünmez; Git yalnızca **farkları**
gösterir. Bir dosyanın listede olmaması "her şey yolunda" demek.
