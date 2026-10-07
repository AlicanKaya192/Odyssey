# İyi Alışkanlıklar

Git'in komutlarını artık biliyorsun. Bu bölüm komutlardan çok **nasıl
kullanıldıklarıyla** ilgili: geçmişi okunur tutan commit'ler, iyi mesajlar,
ekiplerin dal düzenleri ve işini hızlandıran birkaç ayar. Bunlar kural değil,
ekiplerin yıllar içinde vardığı alışkanlıklar; geçmişe bakan herkesin (en
çok da birkaç ay sonraki senin) işini kolaylaştırırlar.

## Küçük ve tek işlik commit'ler

İyi bir commit **tek bir şey** anlatır ve kendi başına anlamlıdır.

| Kötü | İyi |
|---|---|
| "Bugünkü işler": yazım düzeltmesi + yeni özellik + biçim değişikliği | Üç ayrı commit |
| Bir haftalık iş tek commit'te | Her mantıklı adımda bir commit |
| Yarım, çalışmayan kod `main`'de | Yarım iş dalda; `main` hep çalışır |

Neden?

- Bir hatanın **hangi değişiklikle** geldiği kolayca bulunur.
- Tek bir değişikliği **geri almak** (`git revert`) diğerlerini bozmaz.
- Gözden geçiren kişi neyi neden yaptığını anlar.

Commit'ten önce `git diff --staged` ile ne gireceğine bak (03); iki ayrı iş
varsa `git add dosya` ile ayır (02).

## Commit mesajı

<figure class="fig">
  <pre><code class="language-text">Fix crash when the cart is empty

The total was divided by the item count, which is
zero for an empty cart. Return 0 instead.</code></pre>
  <div class="anat">
    <div class="anat-row"><span>Başlık</span><span>Kısa (≤ 50 karakter), emir kipiyle, sonunda nokta yok. git log --oneline bunu gösterir.</span></div>
    <div class="anat-row"><span>Boş satır</span><span>Başlığı açıklamadan ayırır.</span></div>
    <div class="anat-row"><span>Açıklama</span><span>Neden yapıldı? Fark ne yapıldığını zaten gösteriyor.</span></div>
  </div>
  <figcaption>İyi bir commit mesajının üç parçası.</figcaption>
</figure>

Kurallar:

1. **Başlık kısa** (50 karakter civarı), sonunda nokta yok.
2. **Emir kipi**: `Add`, `Fix`, `Remove`, `Update`, `Rename`. "Bu commit
   uygulanırsa…" cümlesini tamamlar: *…Add search box*.
3. Gerekirse **boş bir satırdan sonra açıklama**: ne değişti değil (onu fark
   gösteriyor), **neden** değişti.

Terminalde iki paragraf için `-m` iki kez yazılır:

```text
~/site (main) $ echo "<h1>Home</h1>" > index.html
~/site (main) $ git commit -am "Fix title typo" -m "Visitors reported it."
[main b88cfa3] Fix title typo
 1 file changed, 1 insertion(+), 1 deletion(-)
~/site (main) $ git log -1
commit b88cfa3ac7cde15a179e77f0116e09a7d444d042 (HEAD -> main)
Author: Ada Lovelace <ada@example.com>
Date:   Wed Oct 7 10:01:00 2026 +0300

    Fix title typo
    
    Visitors reported it.
~/site (main) $ git log --oneline
b88cfa3 (HEAD -> main) Fix title typo
772525a Add home page
```

| Kötü mesaj | Neden kötü | Daha iyisi |
|---|---|---|
| `fix` | Neyi? | `Fix crash when the cart is empty` |
| `update index.html` | Dosya adını fark zaten söylüyor | `Add opening hours to the home page` |
| `asdf`, `wip`, `.` | Hiçbir şey söylemiyor | (birleştir ya da yeniden adlandır) |
| `Fixed bugs and added stuff` | İki iş, belirsiz | İki commit, iki net başlık |

## Conventional Commits (isteğe bağlı)

Bazı ekipler başlığın başına türünü yazar; araçlar bundan sürüm notu
üretir:

| Önek | Anlamı |
|---|---|
| `feat:` | Yeni özellik |
| `fix:` | Hata düzeltmesi |
| `docs:` | Yalnızca belge |
| `refactor:` | Davranışı değiştirmeyen kod düzenlemesi |
| `test:` | Testler |
| `chore:` | Bakım işleri (bağımlılık, ayar) |

Örnek: `feat: add dark mode`, `fix: handle empty cart`. Ekibin kullanıyorsa
uy; kullanmıyorsa şart değil.

## Dal düzenleri

| Düzen | Nasıl | Kime uygun |
|---|---|---|
| **GitHub Flow** | `main` + kısa ömürlü özellik dalları + PR | Çoğu proje, sürekli yayın |
| **Git Flow** | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` | Belirli tarihlerde sürüm çıkan ürünler |
| **Trunk-based** | Herkes çok sık, çok küçük commit'lerle doğrudan `main`'e (özellik bayraklarıyla) | Güçlü otomatik testi olan ekipler |

Bilmiyorsan **GitHub Flow** ile başla: bu patikada öğrendiğin her şey ona
göre.

## Günlük akış

```text
git switch main && git pull           güncel main
git switch -c add-faq                 işe dal aç
... küçük commit'ler ...
git push -u origin add-faq            gönder, PR aç
... gözden geçirme, birleştirme ...
git switch main && git pull           birleştirilmiş main
git branch -d add-faq                 temizle
```

## Zaman kazandıran ayarlar

| Ayar | Ne yapar |
|---|---|
| `git config --global alias.lg "log --oneline --graph --all"` | `git lg` kısaltması. |
| `git config --global alias.st "status -s"` | `git st`. |
| `git config --global pull.rebase true` | `pull` yerel commit'leri gelenlerin üstüne dizer (12). |
| `git config --global fetch.prune true` | Her fetch silinen uzak dalları temizler. |
| `git config --global push.autoSetupRemote true` | Yeni dalda ilk `git push` için `-u origin dal` yazmaya gerek kalmaz. |

Kısaltma bir kez tanımlanır, sonra komut gibi kullanılır:

```text
~/site (main) $ git config --global alias.lg "log --oneline --graph --all"
~/site (main) $ git lg
* 772525a (HEAD -> main) Add home page
~/site (main) $ git config --global alias.st "status -s"
~/site (main) $ echo "x" >> index.html
~/site (main) $ git st
 M index.html
```

## Yanlış yazınca

Git yanlış yazılan komutta en yakınını önerir; mesajı oku:

```text
~/site (main) $ git comit
git: 'comit' is not a git command. See 'git --help'.

The most similar command is
        commit
~/site (main) $ git stauts
git: 'stauts' is not a git command. See 'git --help'.

The most similar command is
        status
```

Bir komutun seçeneklerini unuttuysan gerçek terminalde `git <komut> -h` kısa,
`git help <komut>` uzun yardım verir.

## Bir de bunlar

- **Sırları hiç commit'leme** ve `.gitignore`'u ilk commit'ten önce yaz (05).
- **Paylaşılmış geçmişi yeniden yazma** (12): `--amend`, `rebase`, `reset`
  yalnızca sende olan commit'lerde.
- **Sık push et.** Bilgisayarındaki commit yedeklenmiş sayılmaz.
- **Önce `git status`.** Bu patikanın ilk günden beri en önemli alışkanlığı.

## Özet

- Commit küçük, tek işlik ve kendi başına anlamlı olsun.
- Mesaj: kısa, emir kipiyle başlık; gerekirse boş satırdan sonra "neden".
- Conventional Commits bir seçenek (`feat:`, `fix:`).
- Dal düzeni bilmiyorsan GitHub Flow.
- Kısaltmalar ve `pull.rebase`, `fetch.prune`, `push.autoSetupRemote` gibi
  ayarlar zaman kazandırır.
