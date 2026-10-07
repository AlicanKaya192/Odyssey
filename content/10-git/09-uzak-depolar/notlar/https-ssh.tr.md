GitHub'a iki yoldan bağlanılır. Deponun sayfasındaki yeşil **Code**
düğmesi ikisinin adresini de verir.

| | HTTPS | SSH |
|---|---|---|
| Adres | `https://github.com/ada/notes.git` | `git@github.com:ada/notes.git` |
| Kimlik | Tarayıcıda giriş ya da kişisel erişim anahtarı | Bilgisayardaki SSH anahtarı |
| Kurulum | Windows'ta hiçbiri (Git Credential Manager) | Bir kez anahtar oluşturup GitHub'a eklemek |
| Engel | — | Bazı kurum ağları SSH portunu kapatır |

Başlangıç için **HTTPS** yeterli: ilk `push`'ta tarayıcıda GitHub açılır,
onaylarsın, Git Credential Manager hatırlar.

## SSH anahtarı (isteğe bağlı)

```text
ssh-keygen -t ed25519 -C "ada@example.com"
```

Sorulara Enter ile geçebilirsin (istersen anahtara parola koy). İki dosya
oluşur: `~/.ssh/id_ed25519` (**gizli**, kimseyle paylaşma) ve
`~/.ssh/id_ed25519.pub` (açık). Açık olanın içeriğini GitHub › Settings ›
SSH and GPG keys › New SSH key'e yapıştır. Denemek için:

```text
ssh -T git@github.com
```

`Hi ada! You've successfully authenticated` görürsen tamam. Var olan bir
deponun adresini SSH'ye çevirmek:

```text
git remote set-url origin git@github.com:ada/notes.git
```

## Kişisel erişim anahtarı (token)

Tarayıcı açılamayan yerlerde (sunucular, bazı araçlar) şifre yerine GitHub
› Settings › Developer settings › Personal access tokens'tan bir anahtar
oluşturulur ve şifre sorulan yere o yapıştırılır. Anahtar bir şifredir:
dosyaya, koda ya da commit'e yazılmaz.
