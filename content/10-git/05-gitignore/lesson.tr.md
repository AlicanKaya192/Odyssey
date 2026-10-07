# .gitignore: Görmezden Gelmek

Her projede Git'in **asla** izlememesi gereken dosyalar olur:

- Programın kendi ürettiği dosyalar: `__pycache__/`, `build/`, `.log`
  dosyaları. Kaynak koddan yeniden üretilebilirler; depoda yer kaplar ve her
  çalıştırmada "değişti" görünürler.
- Kişisel ya da gizli dosyalar: şifre ve anahtar içeren `.env`, editörün
  ayar klasörü, sanal ortam (`.venv/`).
- Büyük veri dosyaları: yüzlerce MB'lık `.csv`, model dosyaları.

Bunlar `git status`'ta her seferinde `??` olarak görünür ve `git add .` ile
yanlışlıkla commit'e girebilir. Çözüm: deponun kökünde **`.gitignore`**
adında bir metin dosyası. İçindeki her satır bir **desen**; desene uyan
dosyaları Git görmezden gelir.

## Önce ve sonra

Bir Python projesinde `.gitignore` yokken:

```text
~/app (main) $ git status -s
?? .env
?? __pycache__/
?? app.py
?? build/
?? debug.log
?? error.log
```

Altı satırın yalnızca biri (`app.py`) gerçekten bizim kodumuz. `.gitignore`
yazalım:

```text
~/app (main) $ echo "*.log" > .gitignore
~/app (main) $ echo "build/" >> .gitignore
~/app (main) $ echo ".env" >> .gitignore
~/app (main) $ echo "__pycache__/" >> .gitignore
~/app (main) $ cat .gitignore
*.log
build/
.env
__pycache__/
~/app (main) $ git status -s
?? .gitignore
?? app.py
~/app (main) $ git status -s --ignored
?? .gitignore
?? app.py
!! .env
!! __pycache__/
!! build/
!! debug.log
!! error.log
```

Artık `git status` yalnızca izlenmesi gerekenleri gösteriyor. Görmezden
gelinenler kaybolmadı; klasörde duruyorlar, `--ignored` ile görünürler
(`!!` ile).

**`.gitignore`'un kendisi commit'lenir.** Böylece depoyu alan herkes aynı
kuralları kullanır.

## Desenler

| Desen | Neye uyar |
|---|---|
| `debug.log` | Her klasörde bu addaki dosyaya. |
| `*.log` | `.log` ile biten her dosyaya (`*` "herhangi bir şey"). |
| `build/` | `build` adındaki **klasörlere** ve içindeki her şeye. |
| `/todo.txt` | Yalnızca **kökteki** `todo.txt`'ye (baştaki `/` "buradan başla"). |
| `docs/*.pdf` | Yalnızca `docs` klasöründeki `.pdf`'lere. |
| `**/cache/` | Hangi derinlikte olursa olsun `cache` klasörlerine. |
| `!keep.log` | **İstisna:** yukarıdaki bir kural yakalasa da bunu görmezden gelme. |
| `# not` | Yorum satırı. |

İki ayrıntı:

- Sonda `/` varsa desen **yalnızca klasörlere** uyar. `build/` bir `build`
  dosyasını yakalamaz; `build` ikisini de yakalar.
- Kurallar sırayla okunur, **sonuncusu kazanır**. `!` istisnası bu yüzden
  genel kuralın **altına** yazılır.

```text
~/app (main) $ git status -s
?? .gitignore
?? app.py
~/app (main) $ echo '!keep.log' >> .gitignore
~/app (main) $ git status -s
?? .gitignore
?? app.py
?? keep.log
```

`!` içeren satırı terminalde **tek tırnakla** yaz: `echo '!keep.log' >> .gitignore`.
Bash çift tırnağın içindeki `!` işaretini önceki komutlara gönderme sanır ve
`event not found` hatası verir.

> Bir klasörün tamamı görmezden gelinirse içindeki bir dosyayı `!` ile geri
> alamazsın: Git o klasörün içine hiç bakmaz. `logs/` yerine `logs/*` yazıp
> `!logs/keep.txt` eklersen olur.

## Neden görmezden geliniyor? `git check-ignore -v`

Bir dosyanın neden görünmediğini bulamıyorsan Git'e sor:

```text
~/app (main) $ git check-ignore -v debug.log
.gitignore:1:*.log      debug.log
~/app (main) $ git check-ignore -v build/app.exe
.gitignore:2:build/     build/app.exe
~/app (main) $ git check-ignore -v app.py
```

Çıktı: hangi dosya (`.gitignore`), kaçıncı satır ve hangi desen. Görmezden
gelinmeyen bir dosya için hiçbir şey yazmaz.

## Yine de eklemek: `git add -f`

Görmezden gelinen bir dosyayı adıyla eklemeye çalışırsan Git uyarır. Gerçekten
istiyorsan `-f` (*force*):

```text
~/app (main) $ git add debug.log
The following paths are ignored by one of your .gitignore files:
debug.log
hint: Use -f if you really want to add them.
hint: Disable this message with "git config set advice.addIgnoredFile false"
~/app (main) $ git add -f debug.log
~/app (main) $ git status -s
A  debug.log
?? .gitignore
?? app.py
```

## Zaten izlenen dosya

`.gitignore` yalnızca **izlenmeyen** dosyaları etkiler. Bir dosya bir kez
commit'lendiyse onu `.gitignore`'a yazmak yetmez; Git değişikliklerini
göstermeye devam eder. Önce izlemeyi bırakmak gerekir: `git rm --cached`
(dosya klasörde kalır).

```text
~/app (main) $ echo "settings.local.json" > .gitignore
~/app (main) $ git status -s
 M settings.local.json
?? .gitignore
~/app (main) $ git rm --cached settings.local.json
rm 'settings.local.json'
~/app (main) $ git add .gitignore
~/app (main) $ git status -s
A  .gitignore
D  settings.local.json
~/app (main) $ git commit -m "Stop tracking local settings"
[main c67c262] Stop tracking local settings
 2 files changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 .gitignore
 delete mode 100644 settings.local.json
~/app (main) $ git status -s
~/app (main) $ ls
app.py  settings.local.json
```

Bundan sonra `settings.local.json` klasörde kalıyor ama Git onu görmüyor.

> ⚠ **Gizli bilgi bir kez commit'lendiyse** (şifre, API anahtarı) dosyayı
> `.gitignore`'a yazmak onu **geçmişten silmez**: eski commit'lerde hâlâ
> duruyor. Depo GitHub'a gittiyse o şifreyi hemen **değiştir**; artık açığa
> çıkmış say. En iyisi `.env` gibi dosyaları ilk commit'ten önce
> `.gitignore`'a yazmak.

## Hazır şablonlar

Her dil ve araç için hazır `.gitignore` şablonları var: GitHub'ın
`github/gitignore` deposu ve GitHub'da yeni depo açarken çıkan "Add
.gitignore" seçeneği. Bir Python / veri bilimi projesi için tipik bir başlangıç:

```text
# Python
__pycache__/
*.pyc
.venv/

# Gizli ayarlar
.env

# Jupyter
.ipynb_checkpoints/

# Büyük veri ve çıktılar
data/raw/
*.parquet
models/

# Editör ve işletim sistemi
.vscode/
.DS_Store
Thumbs.db
```

## Yalnızca senin bilgisayarında

`.gitignore` herkesle paylaşılır. Yalnızca seni ilgilendiren desenler için
iki yer daha var:

- `.git/info/exclude`: aynı biçimde, ama yalnızca bu depo ve yalnızca sende
  (commit'lenmez).
- Genel dosya: `git config --global core.excludesFile ~/.gitignore_global`
  ile bütün depoların için (ör. işletim sisteminin `Thumbs.db`'si).

## Özet

- `.gitignore` deponun kökünde; her satır bir desen. Kendisi commit'lenir.
- `*` her şey, sonda `/` yalnızca klasör, başta `/` yalnızca kök, `**/` her
  derinlik, `!` istisna; son eşleşen kural kazanır.
- `git status --ignored` görmezden gelinenleri, `git check-ignore -v dosya`
  sebebini gösterir.
- `git add -f` görmezden gelineni yine de ekler.
- Zaten izlenen dosya için önce `git rm --cached`.
- Commit'lenmiş bir şifre `.gitignore` ile kurtarılmaz: değiştir.
