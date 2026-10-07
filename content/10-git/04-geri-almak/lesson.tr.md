# Geri Almak

Git'i kullanmanın asıl sebebi şu: **hata yapmaktan korkmamak**. Yanlış bir
dosyayı sildin, bir commit'e eksik dosya koydun, bir değişiklik her şeyi
bozdu... Hepsinin bir geri dönüş yolu var. Bu bölümde hangi durumda hangi
komutun kullanıldığını göreceğiz.

Önce önemli bir uyarı: geri alma komutlarının bazıları **commit'lenmemiş**
işi kalıcı olarak siler. Git yalnızca commit'lenmiş şeyi koruyabilir. O
komutların yanına ⚠ koyduk.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Dosyada (henüz eklenmedi)</span><span>git restore dosya — değişikliği atar ⚠</span></div>
    <div class="anat-row"><span>Hazırlık alanında</span><span>git restore --staged dosya — hazırlıktan çıkarır, değişiklik kalır</span></div>
    <div class="anat-row"><span>Son commit'te</span><span>git commit --amend — son commit'i düzeltir</span></div>
    <div class="anat-row"><span>Commit'lerde (yalnızca sende)</span><span>git reset — dalı geri taşır</span></div>
    <div class="anat-row"><span>Paylaşılmış commit'te</span><span>git revert — tersini yapan yeni commit</span></div>
  </div>
  <figcaption>Önce sor: geri almak istediğim şey nerede? Komut ona göre seçilir.</figcaption>
</figure>

## 1. Dosyadaki değişikliği at: `git restore`

Bir dosyayı düzenledin, beğenmedin, son commit'teki hâline dönmek
istiyorsun:

```text
~/notes (main) $ echo "oops" > todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git restore todo.txt
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
~/notes (main) $ git status -s
```

`git status` zaten söylüyordu: `use "git restore <file>..." to discard
changes`. ⚠ Atılan değişiklik geri gelmez; hiçbir yere kaydedilmemişti.

> Eski kaynaklarda aynı iş için `git checkout -- dosya` yazar. Hâlâ çalışır,
> ama `checkout` dal değiştirmek gibi başka işler de yaptığı için Git 2.23'te
> daha açık olan `restore` ve `switch` geldi. Biz yenilerini kullanacağız.

## 2. Hazırlık alanından çıkar: `git restore --staged`

Bir değişikliği `git add` ile ekledin ama bu commit'e girmesini
istemiyorsun. Değişiklik **dosyada kalır**, yalnızca hazırlık alanından
çıkar:

```text
~/notes (main) $ echo "Buy eggs" >> todo.txt
~/notes (main) $ git add todo.txt
~/notes (main) $ git status -s
M  todo.txt
~/notes (main) $ git restore --staged todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
Buy eggs
```

Bu güvenlidir: hiçbir şey silinmez. Yeni (hiç commit'lenmemiş) bir dosyada
02'de gördüğümüz `git rm --cached` aynı işi yapar.

## 3. Son commit'i düzelt: `git commit --amend`

En sık yapılan iki hata: mesajda yazım hatası, ya da bir dosyayı eklemeyi
unutmak. İkisi de son commit'i yeniden yazarak düzelir.

Mesajı değiştirmek:

```text
~/notes (main) $ git log --oneline -2
820b3f1 (HEAD -> main) Add brad
f2dfe4a Add readme
~/notes (main) $ git commit --amend -m "Add bread"
[main b898dbd] Add bread
 Date: Wed Oct 7 10:04:00 2026 +0300
 1 file changed, 1 insertion(+)
~/notes (main) $ git log --oneline -2
b898dbd (HEAD -> main) Add bread
f2dfe4a Add readme
```

Unutulan dosyayı eklemek: önce `git add`, sonra `--amend --no-edit`
("mesaja dokunma"):

```text
~/notes (main) $ git status -s
?? plan.txt
~/notes (main) $ git log --oneline -1
744ea10 (HEAD -> main) Plan the week
~/notes (main) $ git add plan.txt
~/notes (main) $ git commit --amend --no-edit
[main 17622b9] Plan the week
 Date: Wed Oct 7 10:04:00 2026 +0300
 2 files changed, 2 insertions(+)
 create mode 100644 plan.txt
~/notes (main) $ git log --oneline -1
17622b9 (HEAD -> main) Plan the week
~/notes (main) $ git show --stat
commit 17622b994a10ce90c75bcc8039fb9f3e681d9259 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:04:00 2026 +0300

    Plan the week

 plan.txt | 1 +
 todo.txt | 1 +
 2 files changed, 2 insertions(+)
```

Commit sayısı aynı kaldı ama hash değişti (`--amend` eski commit'i
düzenlemez, yerine yenisini koyar). ⚠ Bu yüzden **başkalarıyla paylaştığın**
(GitHub'a gönderdiğin) bir commit'i `--amend` ile değiştirme; 09'da
nedenini göreceğiz.

## 4. Dosyanın eski bir hâlini geri getir

`git restore --source=<commit> dosya` dosyayı o commit'teki hâline
getirir. Yalnızca o dosya değişir; geçmiş olduğu gibi kalır ve değişikliği
istersen commit'lersin:

```text
~/notes (main) $ git restore --source=HEAD~2 todo.txt
~/notes (main) $ cat todo.txt
Buy milk
~/notes (main) $ git status -s
 M todo.txt
```

## 5. İzlenen dosyayı silmek ve adını değiştirmek

Git'in izlediği bir dosyayı `rm` ile silersen Git bunu "silinmiş ama
hazırlanmamış" bir değişiklik olarak görür; ayrıca `git add` gerekir.
`git rm` ikisini birden yapar. Ad değiştirmede de aynısı: `git mv`.

```text
~/notes (main) $ git mv readme.md README.md
~/notes (main) $ git status -s
R  readme.md -> README.md
~/notes (main) $ rm todo.txt
~/notes (main) $ git status -s
R  readme.md -> README.md
 D todo.txt
~/notes (main) $ git restore todo.txt
~/notes (main) $ git rm todo.txt
rm 'todo.txt'
~/notes (main) $ git status -s
R  readme.md -> README.md
D  todo.txt
~/notes (main) $ ls
README.md
```

## 6. İzlenmeyen dosyaları temizle: `git clean`

Derleme çıktısı, geçici dosyalar... Git'in hiç izlemediği dosyaları topluca
silmek için `git clean`. Git seni korumak için `-f` (*force*) olmadan
çalışmaz; önce **`-n` ile ne silineceğine bak**:

```text
~/notes (main) $ git status -s
?? build/
?? cache.tmp
~/notes (main) $ git clean
fatal: clean.requireForce is true and -f not given: refusing to clean
~/notes (main) $ git clean -n
Would remove cache.tmp
~/notes (main) $ git clean -nd
Would remove build/
Would remove cache.tmp
~/notes (main) $ git clean -fd
Removing build/
Removing cache.tmp
~/notes (main) $ git status -s
```

`-d` izlenmeyen klasörleri de siler. ⚠ `git clean` ile silinen dosyalar hiç
commit'lenmemiştir; geri getirilemez.

## 7. Commit'leri geri al: `git reset`

`git reset` dalı **geriye taşır**: son commit'ler daldan çıkar. Asıl soru
o commit'lerdeki değişikliklere ne olacağı; bunu üç kip belirler:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>git reset --soft HEAD~1</span><span>Commit daldan çıkar. Değişiklik hazırlık alanında, commit'e hazır.</span></div>
    <div class="anat-row"><span>git reset HEAD~1</span><span>(--mixed) Commit çıkar. Değişiklik dosyada, hazırlanmamış.</span></div>
    <div class="anat-row"><span>git reset --hard HEAD~1</span><span>Commit çıkar, değişiklik silinir. Dosyalar önceki commit'e döner. ⚠</span></div>
  </div>
  <figcaption>Üçünde de dal bir commit geri gider; fark, değişikliğin nerede kaldığı.</figcaption>
</figure>

```text
~/notes (main) $ git log --oneline -2
1d5cec5 (HEAD -> main) Add bread
f2dfe4a Add readme
~/notes (main) $ git reset --soft HEAD~1
~/notes (main) $ git status -s
M  todo.txt
~/notes (main) $ git commit -m "Add bread"
[main b898dbd] Add bread
 1 file changed, 1 insertion(+)
~/notes (main) $ git reset HEAD~1
Unstaged changes after reset:
M       todo.txt
~/notes (main) $ git status -s
 M todo.txt
~/notes (main) $ git commit -am "Add bread"
[main 9b9aedd] Add bread
 1 file changed, 1 insertion(+)
~/notes (main) $ git reset --hard HEAD~1
HEAD is now at f2dfe4a Add readme
~/notes (main) $ git status -s
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

- `--soft`: commit gitti, değişiklik **hazırlık alanında** bekliyor.
  "Son iki commit'i tek commit yapayım" gibi işler için.
- `--mixed` (seçenek yazmazsan bu): değişiklik **dosyada**, hazırlanmamış.
- ⚠ `--hard`: değişiklik **tamamen gider**; dosyalar o commit'teki hâline
  döner. Commit'lenmemiş işin de silinir.

`git reset --hard` (commit vermeden) "son commit'ten bu yana yaptığım her
şeyi at" demektir; ⚠ en tehlikeli geri alma budur.

> Commit'i `reset --hard` ile attın ve pişman oldun mu? Commit'ler hemen
> silinmez; bölüm 14'te `git reflog` ile geri getirmeyi göreceğiz.

## 8. Paylaşılmış commit'i geri al: `git revert`

`reset` geçmişi değiştirir: commit'ler daldan çıkar. Kendi bilgisayarındaki
commit'ler için sorun yok, ama başkalarının da aldığı bir commit'i
silersen onların geçmişiyle seninki ayrışır.

`git revert <commit>` geçmişe dokunmaz: o commit'in **tersini yapan yeni
bir commit** ekler.

```text
~/notes (main) $ git revert HEAD --no-edit
[main 3f6b747] Revert "Add bread"
 1 file changed, 1 deletion(-)
~/notes (main) $ git log --oneline -3
3f6b747 (HEAD -> main) Revert "Add bread"
1d5cec5 Add bread
f2dfe4a Add readme
~/notes (main) $ cat todo.txt
Buy milk
Call Ada
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>git reset HEAD~1</h4><p>A → B → C</p><p>sonra: A → B</p><p>C geçmişten çıktı</p><p><b>Yalnızca sendeki commit'ler için</b></p></div>
    <div class="ok"><h4>git revert HEAD</h4><p>A → B → C</p><p>sonra: A → B → C → C'</p><p>C' C'nin tersini yapar</p><p><b>Paylaşılmış geçmiş için</b></p></div>
  </div>
  <figcaption>reset geçmişi siler, revert geçmişe ekler. Sonuçta dosyalar ikisinde de aynı.</figcaption>
</figure>

## Hangi durumda hangisi?

| Durum | Komut |
|---|---|
| Dosyadaki değişikliği at | ⚠ `git restore dosya` |
| Hazırlık alanından çıkar | `git restore --staged dosya` |
| Son commit'in mesajını düzelt | `git commit --amend -m "Yeni"` |
| Son commit'e unutulan dosyayı ekle | `git add dosya` + `git commit --amend --no-edit` |
| Dosyanın eski hâlini getir | `git restore --source=HEAD~2 dosya` |
| İzlenen dosyayı sil / taşı | `git rm dosya` / `git mv eski yeni` |
| İzlenmeyen dosyaları sil | `git clean -n`, sonra ⚠ `git clean -f` |
| Son commit'leri geri al, değişiklik kalsın | `git reset HEAD~1` (`--soft` hazırlıkta tutar) |
| Son commit'leri tamamen at | ⚠ `git reset --hard HEAD~1` |
| Paylaşılmış bir commit'i geri al | `git revert <commit>` |

## Özet

- Commit'lenmemiş iş korunmaz: `restore`, `clean -f`, `reset --hard` onu
  kalıcı olarak siler.
- `restore` dosyaya, `restore --staged` hazırlık alanına bakar.
- `--amend` son commit'i yenisiyle değiştirir; paylaşılmış commit'te
  kullanma.
- `reset` dalı geri taşır: `--soft` hazırlıkta, `--mixed` dosyada tutar,
  `--hard` atar.
- `revert` geçmişi bozmadan tersini yapan yeni commit ekler; paylaşılmış
  geçmiş için doğru yol.
