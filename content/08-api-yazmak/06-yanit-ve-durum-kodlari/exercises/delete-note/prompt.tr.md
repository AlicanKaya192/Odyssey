`notes` sözlüğü ve `GET /notes` hazır.

**Yapman gereken:** `DELETE /notes/{note_id}` notu silsin ve gövdesiz `204`
döndürsün. Not yoksa `404` (`"Note not found"`).

- `DELETE /notes/2` → `204`
- `GET /notes` → `{"1": "buy milk", "3": "read Dune"}`
- `DELETE /notes/2` → `404`

`raise HTTPException(status_code=404, detail="...")` bir hata cevabı
gönderir (ayrıntısı Hata Yanıtları bölümünde).
