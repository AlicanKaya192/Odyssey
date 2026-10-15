Bu hat `main`'e her gönderimde paketi derliyor. Yalnızca sürüm etiketinde çalışsın ve yanlış numaralı paket derlenmesin:

- `main` dalı yerine yalnızca `v` ile başlayan etiketler hattı başlatsın (`tags: ["v*"]`).
- Derlemeden **önce** numara denetimi çalışsın: `python scripts/check_version.py "$GITHUB_REF_NAME"`.
