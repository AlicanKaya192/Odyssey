Bir API isteği yöntem, yol ve gövdeden oluşur. `sign_request(key_hex,
method, path, body)` bu üç parçayı **satır sonuyla** (`\n`) alt alta
birleştirip HMAC-SHA256 etiketini onaltılık döndürsün. Parçalardan biri
değişince etiket değişmeli.

**Beklenen çıktı:**

```
5f917ac08d569fdd
True
False
```
