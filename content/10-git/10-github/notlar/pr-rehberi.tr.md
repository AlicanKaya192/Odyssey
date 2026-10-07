İyi bir pull request'i gözden geçirmek kolaydır ve hızlı birleştirilir.

## Açmadan önce

- Dal `main`'in güncel hâlinden mi açıldı? Değilse `main`'i dalına birleştir.
- PR **tek bir işi** mi anlatıyor? İki ayrı iş iki PR.
- Gereksiz dosya, hata ayıklama satırı, yorum satırına alınmış kod kaldı mı?
- Program çalışıyor mu, testler geçiyor mu?

## Başlık ve açıklama

Başlık commit mesajı gibi: kısa, ne yaptığını söyleyen (`Add contact form`).
Açıklama için bir kalıp:

```text
## Ne değişti?
İletişim sayfasına form eklendi; gönderilen mesaj e-postayla geliyor.

## Neden?
Ziyaretçiler bize ulaşmak için e-posta adresini kopyalamak zorundaydı.

## Nasıl denenir?
1. /contact sayfasını aç
2. Formu doldurup gönder

Fixes #12
```

## Gözden geçirme sırasında

- Yorumlar kişiye değil koda. Bir öneri yazarken nedenini de yaz.
- İstenen değişikliği **aynı dalda** yap ve push et; PR güncellenir.
- Bir yoruma cevap verdiysen ya da düzelttiysen **Resolve conversation**.

## Birleştirdikten sonra

```text
git switch main
git pull
git branch -d dal-adi      # squash ile birleştiyse -D
git fetch --prune
```

## Birleştirme seçeneği hangisi?

| Seçenek | Geçmişte | Ne zaman |
|---|---|---|
| Merge commit | Dalın bütün commit'leri + birleştirme commit'i | Dalın adımları anlamlıysa. |
| Squash and merge | Tek commit | Dalda çok sayıda "wip", "fix" commit'i varsa. |
| Rebase and merge | Dalın commit'leri düz çizgide | Düz geçmiş isteyen ekiplerde. |

Ekip çoğu zaman birini seçer ve Settings'te diğerlerini kapatır.
