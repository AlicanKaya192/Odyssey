## Ayırt etmek için üç soru

1. **Kendi kendine yayılıyor mu?** Evet → solucan. Bir dosyaya eklenip
   kullanıcının açmasını mı bekliyor? → virüs.
2. **Kendini yararlı bir program gibi mi gösteriyor?** → truva atı.
3. **Ne yapıyor?** Şifreleyip para istiyor → fidye yazılımı; bilgi
   topluyor → casus yazılım; tuşları kaydediyor → tuş kaydedici;
   gizleniyor → rootkit; uzaktan komut alıyor → bot.

## Türler tek satırda

| Tür | Tek satır |
|---|---|
| Virüs (virus) | Taşıyıcı dosya + kullanıcı ister |
| Solucan (worm) | Ağdan kendi kendine yayılır |
| Truva atı (trojan) | Aldatarak kurulur |
| Fidye yazılımı (ransomware) | Şifreler, para ister |
| Casus yazılım (spyware) | Gizlice bilgi toplar |
| Tuş kaydedici (keylogger) | Tuşları kaydeder |
| Reklam yazılımı (adware) | İstenmeyen reklam |
| Rootkit | Kendini gizler |
| Arka kapı (backdoor) | Gizli geri dönüş yolu |
| Bot / bot ağı (botnet) | Uzaktan yönetilen makineler |
| Kripto madencisi (cryptojacking) | İşlemciyi çalar |
| Dosyasız zararlı (fileless) | Bellekte, dosya bırakmadan |

## Tespit

| Yaklaşım | Güçlü yanı | Zayıf yanı |
|---|---|---|
| İmza tabanlı (signature) | Hızlı, az yanlış alarm | Yeni ya da kendini değiştiren türü görmez |
| Davranış tabanlı (behaviour) | Yeniyi yakalar | Yanlış alarm (false positive) verebilir |

**Tehlike göstergesi** (IOC): bilinen kötü dosya özeti, şüpheli alan adı,
beklenmeyen hizmet.

## Yedek

**3-2-1:** 3 kopya, 2 farklı ortam, 1 başka yerde; ayrıca en az 1
bağlantısız ya da değiştirilemez kopya. Yedek düzenli geri yüklenip
denenir.
