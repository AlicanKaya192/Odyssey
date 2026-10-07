Yeni bir bilgisayarda Git'i hazırlamak için sırayla yapılacaklar. Her biri
bir kez yapılır.

## 1. Kurulum

```bash
git --version
```

Sürüm satırı geliyorsa kurulu. Gelmiyorsa:

- **Windows:** git-scm.com → Download for Windows (ya da `winget install --id Git.Git -e --source winget`).
- **Mac:** `git --version` yazınca gelen kurulum önerisini kabul et ya da `brew install git`.
- **Linux:** `sudo apt install git` / `sudo dnf install git`.

## 2. Kimlik

```bash
git config --global user.name "Adın Soyadın"
git config --global user.email "github-epostan@example.com"
```

## 3. Varsayılanlar

```bash
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

## 4. Kontrol

```bash
git config --global --list
```

Beklenen çıktı (değerler seninkiler):

```text
user.name=Ada Lovelace
user.email=ada@example.com
init.defaultbranch=main
core.editor=code --wait
```

Anahtar adlarının küçük harfle yazıldığını gör: `init.defaultBranch` diye
yazdın, Git `init.defaultbranch` diye gösteriyor. Git ayar adlarında büyük
küçük harf ayırmıyor; ikisi aynı ayar.

## Sık yapılan hatalar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `Author identity unknown` | Ad ya da e-posta yok. | 2. adımı yap. |
| Commit'te ad yalnızca `Ada` | Adı tırnaksız yazdın. | `git config --global user.name "Ada Lovelace"` |
| Ayar bir depoda geçerli, ötekinde değil | `--global` yazmayı unuttun; ayar o deponun `.git/config`'ine gitti. | Komutu `--global` ile tekrar yaz; gerekirse depodakini `git config --unset user.name` ile sil. |
| Ayar hiç etki etmiyor | Anahtar adı yanlış: `user.mail`, `user.nmae`. Git yanlış adı da kaydeder, uyarmaz. | `git config --list --show-origin` ile bak, yanlışı `--unset` ile sil. |
| Commit'ler GitHub'da profiline bağlanmıyor | E-posta GitHub'dakiyle aynı değil. | GitHub › Settings › Emails'teki adresi kullan. |
| Mesajsız `git commit` Vim'de takıldı | Varsayılan düzenleyici Vim. | `Esc`, `:q!`, `Enter` ile çık; `core.editor`'ü ayarla. |
