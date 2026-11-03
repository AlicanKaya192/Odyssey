## İki yöntem

| | İmza tabanlı | Anomali tabanlı |
|---|---|---|
| Neye bakar? | Bilinen saldırı kalıpları | Olağandan sapma |
| Yeni saldırı | Kaçırır | Yakalayabilir |
| Yanlış alarm | Az | Çok |
| Bakım | İmzaları güncellemek | Temel çizgiyi yeniden hesaplamak |

## Sonuç tablosu

| | Gerçekten saldırı | Saldırı değil |
|---|---|---|
| **Uyarı var** | Doğru pozitif (TP) | Yanlış pozitif (FP), yanlış alarm |
| **Uyarı yok** | Yanlış negatif (FN), kaçırılan | Doğru negatif (TN) |

- Kesinlik = TP / (TP + FP)
- Duyarlılık = TP / (TP + FN)

## Python kalıpları

- İmza: `re.compile(desen, re.IGNORECASE).search(satir)`.
- Ortalama ve sapma: `statistics.mean`, `statistics.stdev`.
- z skoru: `(deger - ortalama) / sapma`; `abs(z) > 3` sık kullanılan eşik.
- Küme işlemleri: `uyarilar & saldirilar` (TP), `uyarilar - saldirilar` (FP),
  `saldirilar - uyarilar` (FN).
- Anahtara göre sayım: `Counter()` ve `(ip, kullanici)` demeti.

## Akılda tutulacak

- İmza bilineni, anomali olağandışını bulur; ikisi birlikte kullanılır.
- Bölme yapmadan önce payda sıfır mı bak: hiç uyarı yoksa kesinlik
  tanımsızdır.
- Saldırılar seyrek olduğu için küçük yanlış alarm oranı bile çok boş uyarı
  demektir.
- Tek olay yerine örüntüye bak: başarısızlıkların ardından gelen başarı.
- Belgelerde örnek IP için ayrılmış aralıklar kullanılır:
  `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.
