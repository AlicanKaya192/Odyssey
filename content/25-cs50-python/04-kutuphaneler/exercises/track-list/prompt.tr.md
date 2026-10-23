Başlangıç kodundaki `data`, bir müzik API'sinin cevabına benzeyen örnek bir veri (internetten gelmiyor). Önce ilk sonucu `json.dumps(..., indent=2)` ile okunur biçimde yaz. Sonra `resultCount` kadar sonucu numaralı yaz: `1. Track One`.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
{
  "trackName": "Track One",
  "artistName": "Band"
}
1. Track One
2. Track Two
3. Track Three
```
