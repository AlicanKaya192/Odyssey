# Etiketler ve Sürümler

Bir programı yayınladığında o anki hâlini işaretlemek istersin: "kullanıcılara
giden 1.0 sürümü **bu** commit". Sonra hata bildirildiğinde tam o koda dönüp
bakabilmek, iki sürüm arasında neyin değiştiğini görebilmek için.

Git'te bunun aracı **etiket** (*tag*): bir commit'e verilen **kalıcı** bir ad.

## Dal ile etiket farkı

İkisi de bir commit'i gösteren bir ad. Fark şu:

| | Dal | Etiket |
|---|---|---|
| Commit atınca | İlerler | **Yerinde kalır** |
| Ne için | Süren iş | Geçmişteki önemli bir an (sürüm) |
| Örnek | `main`, `login` | `v1.0`, `v2.3.1` |

Bir etiket sonsuza kadar aynı commit'i gösterir; `v1.0` her zaman 1.0 sürümüdür.

## Hafif etiket

En basiti: yalnızca bir ad.

```text
~/app (main) $ git tag v1.0
~/app (main) $ git tag
v1.0
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main, tag: v1.0) Fix search bug
e44c10f Add search
25a8f90 Add prototype
```

`git log` artık o commit'in yanında `tag: v1.0` yazıyor.

## Açıklamalı etiket

Sürümler için önerilen biçim **açıklamalı** (*annotated*) etiket: kim, ne
zaman etiketledi ve bir mesaj. `-a` ile oluşturulur, mesaj `-m` ile:

```text
~/app (main) $ git tag -a v1.1 -m "Search works"
~/app (main) $ git show v1.1 --stat
tag v1.1
Tagger: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:03:00 2026 +0300

Search works

commit 6d6d69be195421861c3a621844b5a374873e9874 (HEAD -> main, tag: v1.1)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:02:00 2026 +0300

    Fix search bug

 app.txt | 1 +
 1 file changed, 1 insertion(+)
```

`git show` önce etiketin bilgisini (etiketleyen, tarih, mesaj), sonra işaret
ettiği commit'i gösteriyor. Hafif etikette ilk kısım yoktur.

| | Hafif | Açıklamalı |
|---|---|---|
| Oluşturma | `git tag v1.0` | `git tag -a v1.0 -m "..."` |
| Sakladığı | Yalnızca ad | Etiketleyen, tarih, mesaj |
| Kullanım | Kişisel, geçici işaretler | Yayınlanan sürümler |

## Eski bir commit'i etiketlemek

Etiketlemeyi unuttuysan sonradan da yapabilirsin; commit'i ver:

```text
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main, tag: v1.1) Fix search bug
e44c10f Add search
25a8f90 Add prototype
~/app (main) $ git tag v0.1 HEAD~2
~/app (main) $ git tag -n
v0.1            Add prototype
v1.1            Search works
```

`git tag -n` her etiketin yanına mesajını (açıklamalı değilse commit
mesajını) yazar.

## Listelemek, silmek

| Komut | Ne yapar |
|---|---|
| `git tag` | Bütün etiketler (abece sırasıyla). |
| `git tag -l "v1.*"` | Desene uyanlar. |
| `git tag -n` | Mesajlarıyla. |
| `git show v1.0` | Etiketin ve commit'in ayrıntısı. |
| `git tag -d v1.0` | Etiketi siler (commit'e dokunmaz). |

Aynı adla ikinci etiket açılamaz; taşımak için önce sil, sonra yeniden aç.

## Etiketleri GitHub'a göndermek

**`git push` etiketleri göndermez.** Ayrıca göndermen gerekir:

```text
~/app (main) $ git tag -a v1.1 -m "Search works"
~/app (main) $ git push
Everything up-to-date
~/app (main) $ git push origin v1.1
To https://github.com/ada/app.git
 * [new tag]         v1.1 -> v1.1
~/app (main) $ git tag v1.0 HEAD~1
~/app (main) $ git push --tags
To https://github.com/ada/app.git
 * [new tag]         v1.0 -> v1.0
```

| Komut | Ne yapar |
|---|---|
| `git push origin v1.1` | Tek bir etiketi gönderir. |
| `git push --tags` | Bütün etiketleri gönderir. |
| `git push origin --delete v1.1` | GitHub'daki etiketi siler. |

> Gönderilmiş bir etiketi değiştirme. Başkaları `v1.0`'ı indirdiyse senin
> yeni `v1.0`'ın onlarınkini değiştirmez; iki farklı "1.0" olur. Hata varsa
> yeni bir sürüm çıkar (`v1.0.1`).

## Sürüm numaraları: SemVer

Çoğu proje **anlamsal sürümleme** (*Semantic Versioning*) kullanır:
`MAJOR.MINOR.PATCH`, örneğin `2.4.1`.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>MAJOR (2.x.x)</span><span>Uyumsuz değişiklik: kullananlar kodunu değiştirmek zorunda.</span></div>
    <div class="anat-row"><span>MINOR (x.4.x)</span><span>Yeni özellik; eski kullanım aynen çalışıyor.</span></div>
    <div class="anat-row"><span>PATCH (x.x.1)</span><span>Hata düzeltmesi; başka hiçbir şey değişmiyor.</span></div>
  </div>
  <figcaption>Bir sayı artınca sağındakiler sıfırlanır: 1.4.2 → 1.5.0 → 2.0.0.</figcaption>
</figure>

Etiket adı çoğu zaman başına `v` alır: `v2.4.1`.

## `git describe`: neredeyim?

`git describe` bulunduğun commit'i en yakın açıklamalı etikete göre anlatır:

```text
~/app (main) $ git log --oneline
6d6d69b (HEAD -> main) Fix search bug
e44c10f (tag: v1.1) Add search
25a8f90 Add prototype
~/app (main) $ git describe
v1.1-1-g6d6d69b
~/app (main) $ git checkout v1.1
Note: switching to 'v1.1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at e44c10f Add search
~/app (e44c10f...) $ git describe
v1.1
~/app (e44c10f...) $ git switch main
Previous HEAD position was e44c10f Add search
Switched to branch 'main'
```

`v1.1-1-g…` "v1.1'den sonra 1 commit, şu an …'deyim" demek (`g` "git"
anlamında bir önek). Program sürümünü otomatik yazdırmak için kullanılır.
`--tags` hafif etiketleri de sayar.

## Etikete geçmek

`git switch` etikete geçmez (etiket dal değil); `git checkout v1.0` geçer
ama HEAD **kopuk** olur: hiçbir dalda değilsin. Eski bir sürümü incelemek
için uygundur; orada iş yapacaksan dal aç (`git switch -c fix-1.0 v1.0`).
Kopuk HEAD'in ayrıntısı 14'te.

## GitHub'da sürüm (Release)

GitHub'daki **Releases** sayfası etiketlerin üstüne kurulu: bir etiket seçer,
başlık ve sürüm notu yazar, indirilebilir dosyalar (kurulum programı gibi)
eklersin. Kullanıcılar programı oradan indirir. (Bu programın güncellemeleri
de böyle yayınlanıyor.)

## Özet

- Etiket bir commit'e verilen kalıcı ad; dal gibi ilerlemez.
- Hafif: `git tag v1.0`. Açıklamalı (sürümler için): `git tag -a v1.0 -m "..."`.
- Eski commit: `git tag v0.9 <commit>`; silmek `git tag -d`.
- Etiketler ayrıca gönderilir: `git push origin v1.0` ya da `--tags`.
- SemVer: MAJOR (uyumsuz) . MINOR (yeni özellik) . PATCH (düzeltme).
- `git describe` en yakın etikete göre konum; etikete geçmek HEAD'i kopuk
  yapar.
