Dosyanın sonuna bir `deploy` işi ekle:

- `build` bitince başlasın.
- Yalnızca **`main` dalına gönderimde** çalışsın; pull request'lerde çalışmasın. Koşulda olay (`github.event_name`) ve dal (`github.ref`) birlikte.
- Makine `ubuntu-latest`; adımlar: kodu çek, sonra `./deploy.sh` çalıştır.
