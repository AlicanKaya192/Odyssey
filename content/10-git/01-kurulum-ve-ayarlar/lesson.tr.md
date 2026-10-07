# Kurulum ve İlk Ayarlar

Alıştırma terminali Git'i taklit ediyor, ama gerçek projelerin için Git'in
kendi bilgisayarında kurulu olması gerekiyor. Bu bölümde Git'i kuracak ve
**bir kez** yapılan ayarları yapacağız: adın, e-postan, yeni depoların dal
adı ve düzenleyicin. Bunlar yapılmadan ilk commit bile atılamıyor.

## Kurulu mu?

Önce bakalım, belki zaten kuruludur. Terminali aç (Windows'ta Başlat
menüsünden **Git Bash** ya da **PowerShell**, Mac'te **Terminal**) ve yaz:

```bash
git --version
```

`git version 2.55.0` gibi bir satır görürsen Git kurulu; kurulum kısmını
atlayabilirsin. "command not found" ya da "tanınmıyor" gibi bir hata alırsan
kurulum gerekiyor.

## Windows'ta kurulum

1. **git-scm.com** adresine git ve **Download for Windows**'a tıkla. İnen
   dosya `Git-2.xx.x-64-bit.exe` gibi bir kurulum programı.
2. Kurulum programını çalıştır. Çok sayıda ekran gelecek; çoğunda varsayılanı
   bırakıp **Next** demen yeterli. Dört ekranda durup bakmaya değer:

| Ekran | Seçim | Neden |
|---|---|---|
| *Choosing the default editor* | **Visual Studio Code** (kuruluysa) ya da **Notepad** | Varsayılan Vim; çıkmayı bilmeyen biri orada sıkışıp kalabiliyor. |
| *Adjusting the name of the initial branch* | **Override…**, ad **main** | Yeni depoların ana dalı `main` olsun; GitHub da öyle. |
| *Adjusting your PATH* | **Git from the command line and also from 3rd-party software** | Git, PowerShell'den ve VS Code'dan da çalışsın. |
| *Configuring the line ending conversions* | **Checkout Windows-style, commit Unix-style** | Satır sonları depoda tek biçimde dursun (aşağıda). |

3. Kurulum bitince Başlat menüsünde **Git Bash** çıkar. Onu aç ve
   `git --version` yaz.

Komut satırını seven biri Windows'un paket yöneticisiyle de kurabilir:

```bash
winget install --id Git.Git -e --source winget
```

## Mac ve Linux'ta kurulum

**Mac:** Terminal'de `git --version` yazman yeterli. Git yoksa macOS
"komut satırı geliştirici araçlarını" kurmayı önerir; **Kur**'a bas. Homebrew
kullanıyorsan `brew install git` en güncel sürümü kurar.

**Linux:** Dağıtımının paket yöneticisini kullan:

```bash
sudo apt install git     # Ubuntu, Debian
sudo dnf install git     # Fedora
```

## Kimsin? `user.name` ve `user.email`

Her commit yazarının adını ve e-postasını taşır (geçen bölümde gördün). Git
bunları senin ayarlarından okur; ayar yoksa commit atmayı reddeder. Ayarsız
bir bilgisayarda ilk commit'te şunu görürsün:

```text
~/notes (main) $ git commit -m "Add todo list"
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'ada@odyssey.(none)')
```

Git ne yapman gerektiğini de söylüyor. Ayarlayalım:

```text
~ $ git config --global user.name "Ada Lovelace"
~ $ git config --global user.email ada@example.com
~ $ git config user.name
Ada Lovelace
~ $ git config user.email
ada@example.com
```

- `git config` ayar okur ve yazar. `--global` "bu bilgisayardaki bütün
  depolarım için" demek.
- Adı **tırnak içinde** yazdık, çünkü içinde boşluk var. Tırnaksız
  yazarsan Git yalnızca `Ada` kısmını alır.
- Bir değeri okumak için değer vermeden yaz: `git config user.name`.
  Ayarlıysa değeri yazar, değilse hiçbir şey yazmaz.

> **E-posta hangisi olmalı?** GitHub kullanacaksan GitHub hesabındaki
> e-postayla aynı olsun; GitHub commit'leri o sayede seninle eşleştiriyor.
> E-postanın herkese açık commit'lerde görünmesini istemiyorsan GitHub'ın
> sana verdiği `…@users.noreply.github.com` adresini kullanabilirsin
> (GitHub › Settings › Emails).

## Yeni depoların dal adı

Git yeni bir depoyu açarken ana dala bir ad verir. Eski sürümler `master`
derdi; bugün çoğu proje ve GitHub `main` kullanıyor. Kurulumda seçmediysen
bir kez ayarla:

```bash
git config --global init.defaultBranch main
```

Bundan sonra her `git init` `main` dalıyla başlar.

## Düzenleyici: `core.editor`

Bazı komutlar (mesajsız `git commit` gibi) yazman için bir düzenleyici açar.
Kurulumda seçmediysen Vim açılır; Vim'den çıkmak için `Esc` sonra `:q` ve
`Enter` gerekir. Bunu bilmeyen biri için sıkıcı bir sürpriz. VS Code
kullanıyorsan:

```bash
git config --global core.editor "code --wait"
```

`--wait` önemli: Git, sen dosyayı kapatana kadar bekler. Onsuz VS Code açılır
açılmaz Git boş bir mesajla devam eder.

> Odyssey'nin alıştırma terminalinde düzenleyici açılmıyor; commit
> mesajlarını hep `-m` ile yazacağız (gelecek bölüm).

## Ayarlar nerede duruyor? Üç düzey

Git ayarları üç yerde tutar. Aynı ayar birden çok yerde varsa **en dar
olan** kazanır:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Sistem (--system)</span><span>Git'in kurulduğu yerdeki dosya. Bilgisayardaki herkes için. Kurulum programı yazar, sen pek dokunmazsın.</span></div>
    <div class="anat-row"><span>Genel (--global)</span><span>~/.gitconfig. Senin bütün depoların için. Adın, e-postan, editörün burada.</span></div>
    <div class="anat-row"><span>Depo (--local)</span><span>.git/config. Yalnızca o depo için. Seçenek yazmazsan git config buraya yazar.</span></div>
  </div>
  <figcaption>Aşağıdaki yukarıdakini ezer: depodaki ayar genel ayardan, genel ayar sistem ayarından önce gelir.</figcaption>
</figure>

Çoğu zaman yalnızca `--global` yeter. Depo düzeyi farklı bir kimlik gereken
durumlar içindir: örneğin iş projelerinde iş e-postanı kullanmak.

```text
~/work (main) $ git config user.email ada@company.example
~/work (main) $ git config --list --show-origin
file:/home/ada/.gitconfig       user.name=Ada Lovelace
file:/home/ada/.gitconfig       user.email=ada@example.com
file:/home/ada/.gitconfig       init.defaultbranch=main
file:.git/config        core.repositoryformatversion=0
file:.git/config        core.filemode=false
file:.git/config        core.bare=false
file:.git/config        core.logallrefupdates=true
file:.git/config        core.symlinks=false
file:.git/config        core.ignorecase=true
file:.git/config        user.email=ada@company.example
~/work (main) $ git config user.email
ada@company.example
```

`--show-origin` her ayarın hangi dosyadan geldiğini gösteriyor. Burada
`user.email` iki yerde var; bu depoda `.git/config`'teki kazanır, başka bir
depoda ise genel ayar geçerli olur.

## Ayarları görmek ve düzeltmek

| Komut | Ne yapar |
|---|---|
| `git config --list` | Geçerli bütün ayarlar (önce genel, sonra depo). |
| `git config --global --list` | Yalnızca genel ayarlar (`~/.gitconfig`). |
| `git config --list --show-origin` | Her ayarın hangi dosyadan geldiğiyle. |
| `git config user.name` | Tek bir ayarın değeri. |
| `git config --global user.name "Yeni Ad"` | Ayarı değiştir (eskisinin üstüne yazar). |
| `git config --global --unset core.editor` | Ayarı sil. |

Ayar dosyaları düz metin, istersen açıp okuyabilirsin:

```text
[user]
	name = Ada Lovelace
	email = ada@example.com
[init]
	defaultBranch = main
[core]
	editor = code --wait
```

## Windows'ta satır sonları

Windows metin dosyalarında satırı iki karakterle bitirir (`CRLF`), Mac ve
Linux tek karakterle (`LF`). Ekip karışıksa bu fark her satırı "değişmiş"
gösterebilir. Kurulumda seçtiğimiz *Checkout Windows-style, commit
Unix-style* seçeneği `core.autocrlf=true` ayarını yapar: depoya `LF` gider,
senin klasörüne `CRLF` gelir. Bir şey yapman gerekmiyor; "LF will be replaced
by CRLF" uyarısını görürsen bunun yüzünden, zararsız.

## Özet

- `git --version` Git'in kurulu olup olmadığını söyler.
- Windows'ta git-scm.com'dan kurulur; editör, `main` dal adı, PATH ve satır
  sonları ekranlarına dikkat.
- Commit atmadan önce bir kez: `user.name` ve `user.email`.
- `init.defaultBranch main` yeni depoların dal adını belirler.
- `core.editor "code --wait"` Git'in VS Code'u kullanmasını sağlar.
- Ayarlar üç düzeyde: sistem, genel (`--global`), depo. Dar olan kazanır.
