Açık anahtarlı kriptografi, bir yönde kolay, öteki yönde çok zor olan
matematik işlemlerine dayanır. Bu bölümün araçları o "kolay" yönü veriyor.

## Kolay yön, zor yön

| Kolay | Zor (bilinen hızlı yol yok) | Nerede |
|---|---|---|
| İki büyük asalı çarpmak: `p * q` | Çarpımdan `p` ve `q`'yu bulmak (çarpanlara ayırma) | RSA |
| `pow(g, x, p)` hesaplamak | Sonuçtan `x`'i bulmak (ayrık logaritma) | Diffie-Hellman |
| Eğri üzerinde bir noktayı `k` kez toplamak | Sonuçtan `k`'yı bulmak | Eliptik eğriler |

Zor yönün zorluğu sayıların **büyüklüğünden** gelir. Bu derslerdeki küçük
oyuncak sayılarla her şey elle bile bulunabilir; gerçek sistemlerde
sayılar yüzlerce basamaklıdır.

## Gerçek sistemlerde boyutlar

| Sistem | Tipik boyut |
|---|---|
| RSA modülü `n` | En az 2048 bit (yaklaşık 617 basamak) |
| Diffie-Hellman asalı `p` | En az 2048 bit |
| Eliptik eğri | 256 bit (ör. P-256, X25519) |
| Simetrik anahtar | 128 ya da 256 bit |

Eliptik eğriler aynı güvenliği çok daha küçük sayılarla sağlar; bu yüzden
bugün anahtar değişiminde çoğunlukla eğriler kullanılır.

## Uyarı

Bu bölümdeki kodlar matematiği görmek içindir. Gerçek açık anahtarlı
kriptografi büyük sayıların yanı sıra dolgu, rastgelelik ve zamanlama
gibi birçok ayrıntı ister; denenmiş bir kütüphaneyle yapılır.
