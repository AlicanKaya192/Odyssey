IV ve nonce aynı işi görür: aynı anahtarla şifrelenen iki mesajın
birbirine benzememesini sağlar. Kurallar kipe göre biraz değişir.

## Ortak kurallar

- **Gizli değildir.** Şifreli metnin başına eklenir, onunla birlikte
  saklanır ya da gönderilir. Alıcı çözmek için ona ihtiyaç duyar.
- **Aynı anahtarla tekrarlanmaz.** Tekrarlanırsa aynı mesaj aynı şifreli
  metni verir ve kip ECB'nin sorununa geri döner (CTR'de daha kötüsü:
  tekrar-anahtar hatası).
- **Kodun içine sabit yazılmaz.** `iv = b"0000000000000000"` gibi bir satır,
  her mesajda aynı IV demektir.

## CBC'de IV

- Benzersiz olması yetmez, **tahmin edilemez** de olmalı.
- Doğru yol: her mesajda `secrets.token_bytes(16)` (ya da `os.urandom(16)`).
- `random` modülü kullanılmaz: gizli ya da tahmin edilmemesi gereken
  değerler için yapılmamıştır.

## CTR ve GCM'de nonce

- Tahmin edilebilir olabilir ama **kesinlikle benzersiz** olmalı.
- İki güvenli yol: her mesajda rastgele nonce ya da kalıcı olarak saklanan,
  hiç geri sarılmayan bir sayaç.
- Sayaç kullanılıyorsa program yeniden başladığında sıfırdan başlamamalı.

## Hızlı kontrol

| Soru | Doğru cevap |
|---|---|
| IV'yi saklamam gerekir mi? | Evet, şifreli metnin yanında |
| IV'yi gizlemem gerekir mi? | Hayır |
| Aynı IV'yi tekrar kullanabilir miyim? | Hayır, aynı anahtarla asla |
| IV'yi nasıl üretirim? | `secrets.token_bytes(16)` |
| ECB'de IV var mı? | Yok, sorunu da bu |
