Bu iş akışında modülde gördüğümüz dört hata var. Hepsini düzelt:

- İzin: `write-all` yerine yalnızca okuma (`contents: read`).
- Süre sınırı: `test` işine `timeout-minutes: 15`.
- Sürümsüz eylem: `actions/checkout` → `actions/checkout@v4`.
- Kod enjeksiyonu: PR başlığı `run:` satırına doğrudan yazılmasın; komut `echo "Testing $TITLE"`, `TITLE` ortam değişkeni `${{ github.event.pull_request.title }}`.
