# Değişiklikleri Görmek

Git'in en büyük faydalarından biri **geçmişe bakabilmek**: neyi değiştirdin,
henüz commit'lemediğin ne var, üç gün önce bu dosya nasıldı, bu satırı kim
yazdı? Bu bölümde Git'e soru sormanın yollarını öğreneceğiz. Hiçbiri bir
şeyi değiştirmez; hepsi yalnızca **gösterir**. Bu yüzden rahatça
deneyebilirsin.

Bu bölümdeki örneklerin hepsi aynı küçük depoda: `notes` klasöründe bir
yapılacaklar listesi (`todo.txt`) ve bir `readme.md`, üç commit.

```text
~/notes (main) $ git log --oneline
f2dfe4a (HEAD -> main) Add readme
ed15a33 Add call
20c376c Add todo list
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

## `git diff`: henüz hazırlanmamış değişiklikler

`git status` hangi dosyanın değiştiğini söyler, **ne** değiştiğini söylemez.
Onu `git diff` gösterir:

```text
~/notes (main) $ echo "Buy bread" >> todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git diff
diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread
```

Çıktı ilk bakışta karışık görünüyor; parça parça okuyalım:

<figure class="fig">
  <pre><code class="language-text">diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread</code></pre>
  <div class="anat">
    <div class="anat-row"><span>diff --git a/… b/…</span><span>Hangi dosyanın farkı. a/ eski hâl, b/ yeni hâl.</span></div>
    <div class="anat-row"><span>index ab0af58..254c209</span><span>Eski ve yeni içeriğin kısa kimlikleri. Okurken atlayabilirsin.</span></div>
    <div class="anat-row"><span>--- / +++</span><span>Eksi işaretli satırlar eski dosyadan, artı işaretliler yeni dosyadan.</span></div>
    <div class="anat-row"><span>@@ -1,2 +1,3 @@</span><span>Parçanın yeri: eskide 1. satırdan 2 satır, yenide 1. satırdan 3 satır.</span></div>
    <div class="anat-row"><span>(boşluk) Buy milk</span><span>Değişmeyen satır; değişikliğin nerede olduğunu göstermek için.</span></div>
    <div class="anat-row"><span>+Buy bread</span><span>Eklenen satır (yeşil). Silinen satır - ile başlar (kırmızı).</span></div>
  </div>
  <figcaption>Bir farkın parçaları. Asıl önemli olan son satırlar: + eklendi, - silindi.</figcaption>
</figure>

Kısaca: **`+` ile başlayan satır eklendi, `-` ile başlayan silindi**,
başında boşluk olan satır değişmedi (yerini göstermek için oradadır). Bir
satırı değiştirmek Git'in gözünde "eskisini sil, yenisini ekle" demektir:

```text
~/notes (main) $ echo "Buy oat milk" > todo.txt
~/notes (main) $ echo "Call Ada" >> todo.txt
~/notes (main) $ git diff
diff --git a/todo.txt b/todo.txt
index ab0af58..76b6afb 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,2 @@
-Buy milk
+Buy oat milk
 Call Ada
```

## Hangi diff neyi karşılaştırır?

`git diff` tek başına **çalışma alanını hazırlık alanıyla** karşılaştırır.
Bu yüzden `git add`'den sonra boş görünür: değişiklik artık iki tarafta da
aynı. Hazırlanmış değişikliği görmek için `--staged` gerekir:

```text
~/notes (main) $ git add todo.txt
~/notes (main) $ git diff
~/notes (main) $ git diff --staged
diff --git a/todo.txt b/todo.txt
index ab0af58..254c209 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1,2 +1,3 @@
 Buy milk
 Call Ada
+Buy bread
```

<figure class="fig">
  <div class="flow">
    <span class="node">Çalışma alanı</span><span class="arrow">↔</span>
    <span class="node acc">git diff</span><span class="arrow">↔</span>
    <span class="node">Hazırlık alanı</span><span class="arrow">↔</span>
    <span class="node acc">git diff --staged</span><span class="arrow">↔</span>
    <span class="node ok">Son commit</span>
  </div>
  <figcaption>git diff ilk ikisini, git diff --staged son ikisini karşılaştırır. git diff HEAD ise çalışma alanını doğrudan son commit'le.</figcaption>
</figure>

`--staged` ile `--cached` aynı şeydir; ikisini de görürsün. Commit atmadan
önce `git diff --staged` yazmak iyi bir alışkanlıktır: commit'e **tam olarak
ne** gireceğini gösterir.

Ayrıntı yerine özet istersen:

| Komut | Gösterir |
|---|---|
| `git diff --stat` | Dosya başına kaç satır değişti. |
| `git diff --name-only` | Yalnızca değişen dosyaların adları. |
| `git diff readme.md` | Yalnızca o dosyanın farkı. |

## `git log`: geçmiş

```text
~/notes (main) $ git log
commit f2dfe4a515f091cc7d1464d0a4aa58e0e52e1f08 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Add readme

commit ed15a3351e08dfbd752a5e9479e4fe56643b06e3
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Add call

commit 20c376c07d02ed31d1fcfbd46189e96dac4cc468
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:00:00 2026 +0300

    Add todo list
```

Her commit için kimlik (*hash*), yazar, tarih ve mesaj. En yeni en üstte.

**Hash** 40 karakterlik bir harf-rakam dizisi; commit'in içeriğinden
hesaplanıyor, bu yüzden her commit'te farklı. Hepsini yazmana gerek yok: ilk
7 karakter (`ed15a33`) Git'e yeter ve `--oneline` de bunu gösterir.

> Gerçek terminalde `git log` uzunsa çıktı bir sayfalayıcıda açılır; alt
> satırda `:` görürsün. Boşlukla ilerler, **`q`** ile çıkarsın.

### Sık kullanılan seçenekler

| Komut | Ne gösterir |
|---|---|
| `git log --oneline` | Commit başına tek satır: kısa hash + mesaj. |
| `git log -n 3` ya da `git log -3` | Yalnızca son 3 commit. |
| `git log --stat` | Her commit'te hangi dosyalar, kaçar satır değişti. |
| `git log -p` | Her commit'in tam farkı (*patch*). |
| `git log -- todo.txt` | Yalnızca bu dosyayı değiştiren commit'ler. |
| `git log --author=Ada` | Yalnızca yazarında "Ada" geçenler. |
| `git log --grep=fix -i` | Mesajında "fix" geçenler; `-i` büyük-küçük harfe bakmaz. |
| `git log --reverse` | Eskiden yeniye. |

Seçenekler birleşir: `git log --oneline --author=Grace -- todo.txt`.

Depoya bir arkadaşımız, Grace de iki commit atmış olsun:

```text
~/notes (main) $ git log --oneline
f0413ac (HEAD -> main) Mention Grace
c0237ac Add garden tasks
f2dfe4a Add readme
ed15a33 Add call
20c376c Add todo list
~/notes (main) $ git log --oneline --author=Grace
f0413ac (HEAD -> main) Mention Grace
c0237ac Add garden tasks
~/notes (main) $ git log --oneline -- readme.md
f0413ac (HEAD -> main) Mention Grace
f2dfe4a Add readme
~/notes (main) $ git log --oneline -i --grep=grace
f0413ac (HEAD -> main) Mention Grace
```

Satırları kendi düzeninle de yazdırabilirsin: `--format` içinde `%h` kısa
hash, `%an` yazar, `%ad` tarih, `%s` mesaj.

```text
~/notes (main) $ git log --format="%h %an: %s"
f0413ac Grace Hopper: Mention Grace
c0237ac Grace Hopper: Add garden tasks
f2dfe4a Ada Lovelace: Add readme
ed15a33 Ada Lovelace: Add call
20c376c Ada Lovelace: Add todo list
```

## HEAD ve geriye saymak

Her commit'i hash ile anmak zorunda değilsin. **HEAD** "şu an bulunduğun
commit" demek (çoğu zaman dalının son commit'i). Ondan geriye `~` ile
sayılır:

<figure class="fig">
  <div class="flow">
    <span class="node">Add todo list<br><small>HEAD~2</small></span><span class="arrow">→</span>
    <span class="node">Add call<br><small>HEAD~1</small></span><span class="arrow">→</span>
    <span class="node acc">Add readme<br><small>HEAD (main)</small></span>
  </div>
  <figcaption>HEAD bulunduğun commit; HEAD~1 bir öncesi, HEAD~2 iki öncesi. Dal adı (main) da o dalın son commit'i demek.</figcaption>
</figure>

Bu adlar hash'in yerine her komutta kullanılabilir.

## `git show`: tek bir commit

`git show` bir commit'in bilgisini ve farkını birlikte gösterir. Ad
vermezsen HEAD'i gösterir:

```text
~/notes (main) $ git show
commit f2dfe4a515f091cc7d1464d0a4aa58e0e52e1f08 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Add readme

diff --git a/readme.md b/readme.md
new file mode 100644
index 0000000..17e0f0d
--- /dev/null
+++ b/readme.md
@@ -0,0 +1 @@
+# Notes
```

İki çok kullanışlı biçim:

- `git show --stat HEAD~1`: o commit'te hangi dosyalar değişti.
- `git show HEAD~2:todo.txt`: dosyanın **o commit'teki** hâli. Dosyayı
  değiştirmez, yalnızca ekrana yazar.

```text
~/notes (main) $ git show --stat HEAD~1
commit ed15a3351e08dfbd752a5e9479e4fe56643b06e3
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Add call

 todo.txt | 1 +
 1 file changed, 1 insertion(+)
~/notes (main) $ git show HEAD~2:todo.txt
Buy milk
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

## İki commit'i karşılaştırmak

`git diff` iki commit de alabilir: "o zamandan bu zamana ne değişti?"

```text
~/notes (main) $ git diff HEAD~2 HEAD --stat
 readme.md | 1 +
 todo.txt  | 1 +
 2 files changed, 2 insertions(+)
~/notes (main) $ git diff HEAD~2 HEAD -- todo.txt
diff --git a/todo.txt b/todo.txt
index dea7672..ab0af58 100644
--- a/todo.txt
+++ b/todo.txt
@@ -1 +1,2 @@
 Buy milk
+Call Ada
```

## `git blame`: bu satırı kim yazdı?

`git blame dosya` her satırın yanına onu **en son** değiştiren commit'i,
yazarı ve tarihi yazar:

```text
~/notes (main) $ git blame todo.txt
^20c376c (Ada Lovelace 2026-10-07 10:00:00 +0300 1) Buy milk
ed15a335 (Ada Lovelace 2026-10-07 10:01:00 +0300 2) Call Ada
c0237aca (Grace Hopper 2026-10-07 10:03:00 +0300 3) Water the plants
```

Başında `^` olan hash deponun ilk commit'idir. Adı kötü görünse de
(*blame* = suçlamak) asıl kullanımı bir satırın **neden** öyle olduğunu
bulmaktır: hash'i alıp `git show` ile o commit'in mesajına bakarsın.

## Özet

- `git diff`: çalışma alanı ↔ hazırlık alanı (henüz eklemediklerin).
- `git diff --staged`: hazırlık alanı ↔ son commit (commit'e girecekler).
- `git diff A B`: iki commit arası.
- `git log` geçmişi gösterir; `--oneline`, `-n`, `--stat`, `-p`, `--author`,
  `--grep`, `-- dosya` ile süzülür.
- `HEAD` bulunduğun commit; `HEAD~1` bir öncesi, `HEAD~2` iki öncesi.
- `git show` bir commit'i, `git show REV:dosya` dosyanın o andaki hâlini
  gösterir.
- `git blame` her satırın son değiştiği commit'i söyler.
