An API where everyone sees only their own notes. The password check
(`check_password`) is ready; `ada`/`lovelace` and `alan`/`enigma`.

**What to do:**

1. `POST /token`: login → `{"access_token": ..., "token_type": "bearer"}`;
   `401` if wrong.
2. A `current_user` dependency (`HTTPBearer`).
3. `POST /notes` → `201`, `{"id": ..., "owner": ..., "text": ...}`.
4. `GET /notes` → only **your own** notes.
5. `DELETE /notes/{id}` → `404` if missing, `403` (`"Not your note"`) if
   someone else's, otherwise `204`.
