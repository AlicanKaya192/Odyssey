`/report` doğru cevap veriyor ama `async def` içinde `time.sleep` var:
aynı anda gelen istekler sıraya diziliyor.

**Yapman gereken:** bekletmeyi olay döngüsünü kilitlemeyen hâline çevir.
Cevap aynı kalsın: `{"rows": 120}`.
