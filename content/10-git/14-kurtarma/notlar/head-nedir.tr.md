HEAD Git'te "şu an buradayım" işaretidir. Çoğu zaman bir **dalı** gösterir:

```text
HEAD → main → 63074be
```

Commit atınca `main` yeni commit'e ilerler, HEAD de `main`'i gösterdiği için
onunla gider. İstem `(main)` der.

## Kopuk hâl

Bir dal yerine doğrudan commit'e geçersen (`git checkout 63074be`,
`git checkout v1.0`, `git checkout HEAD~2`):

```text
HEAD → c1a230e        (hiçbir dal yok arada)
```

Commit atınca HEAD yeni commit'e ilerler ama **hiçbir dal ilerlemez**. Başka
bir dala geçince yeni commit'i gösteren hiçbir ad kalmaz; Git bu yüzden
uyarır.

## Kopuk HEAD'e nasıl düşülür?

| Komut | Neden |
|---|---|
| `git checkout <hash>` | Commit'e geçtin. |
| `git checkout v1.0` | Etiket bir dal değil. |
| `git checkout origin/main` | Uzak izleme dalı senin dalın değil. |
| `git switch --detach <commit>` | Bilerek. |
| Rebase sürerken | Git commit'leri dizerken hiçbir dalda değil (geçici). |

## Kopuk HEAD'den çıkmak

| Ne istiyorsun? | Komut |
|---|---|
| Hiçbir şey yapmadım, geri dön | `git switch -` ya da `git switch main` |
| Burada yaptıklarım kalsın | `git switch -c yeni-dal` |
| Döndüm ama commit'ler kaldı | Uyarıdaki komut: `git branch ad <hash>` |

## `HEAD@{n}` ile `HEAD~n` farkı

- `HEAD~2`: geçmişte iki commit geri (ebeveynin ebeveyni).
- `HEAD@{2}`: HEAD'in **iki hareket önce** bulunduğu yer (reflog'dan). Bir
  checkout da bir reset de hareket sayılır; commit olmayabilir.
