Bir Python projesi için başlangıç `.dockerignore` dosyası. Kopyala,
projende olmayan satırları sil, kendine özel olanları ekle.

```text
# --- Python ---
**/__pycache__
**/*.pyc
**/*.pyo
.venv
venv
*.egg-info
.pytest_cache
.mypy_cache

# --- Git ve editör ---
.git
.gitignore
.vscode
.idea

# --- Gizli ayarlar ---
.env
.env.*
!.env.example

# --- Docker'ın kendi dosyaları ---
Dockerfile*
compose*.yaml
.dockerignore

# --- Veri ve çıktılar ---
data/
*.log
notebooks/
```

## Satırlar neden orada?

| Satır | Neden dışarıda? |
|---|---|
| `__pycache__`, `*.pyc` | Python'un kendi oluşturduğu önbellek; konteyner zaten yeniden oluşturur. |
| `.venv`, `venv` | Bilgisayarındaki sanal ortam; Windows için kurulmuş, Linux konteynerinde çalışmaz ve çok büyük. |
| `.git` | Projenin bütün geçmişi; çalışmak için gerekmez, yüzlerce MB olabilir. |
| `.env` | Şifreler, anahtarlar. **İmaja asla girmemeli.** |
| `!.env.example` | Değersiz örnek dosya girebilir (hangi ayarların gerektiğini gösterir). |
| `Dockerfile*` | Tarifin kendisinin imajda olmasına gerek yok. |
| `data/`, `*.log` | Büyük ve sık değişen dosyalar; veri volume ile verilir (Volume bölümü). |

## `.gitignore` ile aynı mı?

Çok benziyor ama ayrı dosyalar ve kurallar biraz farklı. En önemlisi:
`.gitignore`'da `__pycache__/` her klasörde geçerli, `.dockerignore`'da
yalnızca kökte. Her klasör için `**/__pycache__` yazmak gerekiyor.

## Doğru çalıştığını nasıl anlarsın?

Derleme çıktısındaki bağlam boyutuna bak:

```text
#5 transferring context: 140B done
```

Bu sayı megabaytlarla ölçülüyorsa bir şey içeri sızıyor. İmajın içine
bakmak için:

```text
docker run --rm greeter ls -la /app
```
