Herkesin yalnızca kendi notlarını gördüğü bir API. Şifre denetimi
(`check_password`) hazır; `ada`/`lovelace` ve `alan`/`enigma`.

**Yapman gerekenler:**

1. `POST /token`: giriş → `{"access_token": ..., "token_type": "bearer"}`;
   yanlışsa `401`.
2. `current_user` bağımlılığı (`HTTPBearer`).
3. `POST /notes` → `201`, `{"id": ..., "owner": ..., "text": ...}`.
4. `GET /notes` → yalnızca **kendi** notların.
5. `DELETE /notes/{id}` → yoksa `404`, başkasınınsa `403`
   (`"Not your note"`), yoksa `204`.
