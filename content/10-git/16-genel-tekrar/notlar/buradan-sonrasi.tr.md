Bu patika Git'in günlük kullanımını kapsadı. Daha ileri gitmek istersen
bakılacak konular ve kaynaklar.

## İlk iş: gerçek bir proje

- GitHub'da hesap aç (yoksa), bir depo oluştur.
- Bu patikadaki akışı kendi kodunla uygula: dal, küçük commit'ler, PR,
  birleştirme, etiket.
- Bir açık kaynak projeye küçük bir katkı (yazım düzeltmesi bile olur): fork,
  dal, PR.

## İleri konular

| Konu | Ne işe yarar |
|---|---|
| `git bisect` | Hatayı getiren commit'i ikili aramayla bulur. |
| `git worktree` | Aynı depodan iki dalı ayrı klasörlerde açar. |
| `git submodule` | Bir depoyu başka bir deponun içinde kullanmak. |
| Hooks (`.git/hooks`) | Commit / push öncesi otomatik denetimler (ör. biçimlendirme). |
| `.gitattributes` | Satır sonu, ikili dosya, fark davranışı ayarları. |
| Git LFS | Büyük dosyaları depo dışında tutmak. |
| GitHub Actions | Her push'ta testleri çalıştırmak (CI). |
| İmzalı commit'ler | Commit'in gerçekten senden geldiğini kanıtlamak. |

## Kaynaklar

- **Pro Git** (git-scm.com/book): Git'in resmi kitabı; ücretsiz, Türkçe
  çevirisi de var.
- **git-scm.com/docs**: her komutun tam belgesi (`git help <komut>` da aynısını
  açar).
- **GitHub Docs** (docs.github.com): pull request, Actions, ayarlar.
- **learngitbranching.js.org**: dalları görsel olarak deneyen bir oyun.

## Odyssey'de devam

- **Docker** patikası: projeni her bilgisayarda aynı çalıştırmak.
- **API** patikaları: GitHub'ın kendisi de bir REST API ile kullanılır.
