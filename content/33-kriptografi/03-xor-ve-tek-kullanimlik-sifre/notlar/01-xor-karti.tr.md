## XOR kuralları

| Kural | Anlamı |
|---|---|
| `a ^ b ^ b == a` | Şifreleme ve çözme aynı işlem |
| `a ^ a == 0` | Aynı anahtar iki kez kullanılırsa anahtar yok olur |
| `a ^ 0 == a` | Sıfırla XOR değiştirmez |
| `a ^ b == b ^ a` | Sıra önemli değil |

## Python kalıpları

- İki bayt dizisini XOR'lamak: `bytes(x ^ y for x, y in zip(a, b))`.
- Metinden bayta: `"PAY".encode()`, geri: `b"PAY".decode()`.
- Bayttan onaltılığa: `data.hex()`, geri: `bytes.fromhex(metin)`.
- Gerçek anahtar: `secrets.token_bytes(len(mesaj))`.
- `zip` kısa olanda durur: anahtar kısaysa mesajın sonu **sessizce**
  kesilir. Uzunluğu önce denetle.

## Tek kullanımlık şifrenin dört koşulu

1. Gerçekten rastgele anahtar.
2. Mesaj kadar uzun anahtar.
3. Yalnızca bir kez.
4. Gizli.

## Sızıntılar

| Hata | Saldırganın elde ettiği |
|---|---|
| Anahtarı tekrar kullanmak | `c1 ^ c2 = m1 ^ m2`; birini bilen ötekini okur |
| Bütünlük denetimi koymamak | Biçimi bilinen mesajı bit bit değiştirmek |
| Anahtarı kısa tutup tekrarlamak | Vigenère'nin zayıflığı geri gelir |
