"Ne oldu?" sorusunun komutları. Hiçbiri bir şeyi değiştirmez.

## Ne değişti?

| Soru | Komut |
|---|---|
| Hangi dosyalar değişti? | `git status` / `git status -s` |
| Henüz eklemediğim değişiklikler neler? | `git diff` |
| Commit'e girecek olanlar neler? | `git diff --staged` |
| Son commit'ten beri her şey? | `git diff HEAD` |
| Yalnızca bir dosya? | `git diff -- dosya` |
| Özet olsun | `git diff --stat` / `--name-only` |

## Geçmiş

| Soru | Komut |
|---|---|
| Son commit'ler | `git log --oneline -10` |
| Hangi dosyalar değişmiş? | `git log --stat` |
| Tam farklarla | `git log -p` |
| Bu dosyaya kim, ne zaman dokundu? | `git log --oneline -- dosya` |
| Grace neler yaptı? | `git log --author=Grace` |
| Mesajında "fix" geçenler | `git log --grep=fix -i` |
| Kendi düzenimle | `git log --format="%h %an %s"` |

## Tek bir commit ya da dosyanın eski hâli

| Soru | Komut |
|---|---|
| Son commit'te ne değişti? | `git show` |
| Bu commit'te hangi dosyalar? | `git show --stat <commit>` |
| Dosya iki commit önce nasıldı? | `git show HEAD~2:dosya` |
| İki commit arasında ne değişti? | `git diff <eski> <yeni>` |
| Bu satırı kim, hangi commit'te yazdı? | `git blame dosya` |

## Fark çıktısını okumak

```text
diff --git a/todo.txt b/todo.txt     hangi dosya
index ab0af58..254c209 100644        eski ve yeni içeriğin kimliği
--- a/todo.txt                       eski hâl
+++ b/todo.txt                       yeni hâl
@@ -1,2 +1,3 @@                      eski: 1. satırdan 2 satır, yeni: 1. satırdan 3 satır
 Buy milk                            değişmedi
 Call Ada                            değişmedi
+Buy bread                           eklendi
```

`-` ile başlayan satır silinmiş, `+` ile başlayan eklenmiş. Değiştirilen
satır bir `-` ve bir `+` olarak görünür.
