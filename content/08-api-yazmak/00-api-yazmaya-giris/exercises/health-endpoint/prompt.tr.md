Docker patikasında konteynerin sağlığını `/health` adresinden
denetlemiştik. Şimdi o adresi sen yaz.

**Yapman gereken:** var olan `GET /` dursun; yanına `GET /health` ekle:

```json
{"status": "ok"}
```
