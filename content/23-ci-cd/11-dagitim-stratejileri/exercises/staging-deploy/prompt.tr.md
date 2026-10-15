Hat paketi derleyip `dist` olarak saklıyor. Bir `deploy-staging` işi ekle:

- `build` bitince başlasın, makine `ubuntu-latest`.
- `staging` ortamına bağlansın.
- Kodu çeksin, `dist` artifact'ini `dist` klasörüne indirsin.
- `python scripts/deploy.py staging` çalıştırsın.
