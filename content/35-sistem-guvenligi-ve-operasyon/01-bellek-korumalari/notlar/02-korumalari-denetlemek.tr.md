Korumaların çoğu bugün varsayılan olarak açıktır. Ama "varsayılan" her
zaman "açık" demek değildir: eski bir derleme betiği, bir uyumluluk ayarı
ya da hızlı derlemek için kapatılmış bir bayrak bir korumayı sessizce
kaldırabilir. Bu yüzden korumalar **denetlenir**, varsayılmaz.

## Ne denetlenir?

- **Derleme bayrakları:** kanarya (`-fstack-protector-strong` ya da `/GS`),
  konuma bağımsız derleme (PIE; ASLR'nin programın kendisine de
  uygulanabilmesi için gerekir), DEP uyumluluğu (`/NXCOMPAT`).
- **Çalışan sistem:** işletim sisteminde ASLR ve DEP açık mı, istisna
  listesinde hangi programlar var.
- **Bellek izinleri:** `rwx` bölge açan bir program var mı; varsa gerçekten
  gerekli mi.

## Denetim bir listeye dönüşür

Bir derleme hattında (CI) her yeni sürüm için aynı sorular sorulur. Bunu
elle yapmak yerine bir **kontrol listesi** betiğe dönüştürülür: her
programın özellikleri okunur, eksik korumalar raporlanır, eksik varsa
sürüm durdurulur. Alıştırmalardaki `missing_protections` bu fikrin oyuncak
hâlidir.

| Bulgu | Önem | Ne yapılır? |
|---|---|---|
| Kanarya yok | Yüksek | Derleme bayrağını aç, yeniden derle |
| PIE yok (ASLR eksik) | Yüksek | Konuma bağımsız derle |
| `rwx` bölge var | Orta | Gerekmiyorsa kaldır, gerekiyorsa gerekçeyi yaz |
| CFI yok | Düşük–orta | Destekleniyorsa aç |

## Neden "kapatmak" bir uyarı işaretidir?

Bir koruma neredeyse hiçbir zaman programın doğru çalışması için
kapatılmaz; genellikle eski bir alışkanlık ya da bir uyumluluk sorunu
yüzünden kapanır. İncelemede bir korumanın kapalı olduğu görülürse sorulan
ilk soru "neden?"dir ve cevap yazılı olmalıdır. Gerekçesi olmayan istisna
kaldırılır.

## Sınırlar

- Korumalar yalnızca **bellek** hatalarına karşıdır; SQL enjeksiyonu,
  yanlış yetki ya da sızan parola üzerinde etkileri yoktur.
- Hiçbiri hatayı yok etmez; en iyi ihtimalle programı güvenli biçimde
  durdurur. Durdurmak da bir kullanılabilirlik kaybıdır (CIA üçlüsündeki
  erişilebilirlik); hatanın kendisi yine düzeltilir.
