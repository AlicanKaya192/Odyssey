| | **DAC** | **MAC** | **RBAC** | **ABAC** |
|---|---|---|---|---|
| Açılımı | Discretionary (isteğe bağlı) | Mandatory (zorunlu) | Role-based (rol tabanlı) | Attribute-based (öznitelik tabanlı) |
| Kim karar verir? | Nesnenin sahibi | Sistem | Rolleri tanımlayan yönetici | Yazılı kurallar |
| Neye bakar? | Sahibin isteği | Gizlilik etiketi ve yetki düzeyi | Kişinin rolü | Özne, nesne, eylem, ortam |
| Güçlü yanı | Esnek, kolay | Kişi kuralı delemez | Yönetimi kolay | Çok ince kurallar |
| Zayıf yanı | Sahip yanılır, Truva atı | Katı, zahmetli | Rol patlaması | Karmaşık, denetimi zor |
| Örnek | Dosya paylaşmak | Gizli belgeler | Okulda öğretmen/öğrenci | "Mesai saatinde, kendi bölümünde" |

## Terimler

- **Sahip** (owner): DAC'te nesne üzerinde karar veren kişi.
- **Gizlilik derecesi** (classification): nesnenin etiketi.
- **Yetki düzeyi** (clearance): kişinin etiketi.
- **Truva atı sorunu**: kullanıcının açtığı programın onun bütün
  yetkisiyle çalışması.
- **Rol hiyerarşisi** (role hierarchy): bir rolün başka bir rolün
  izinlerini miras alması.
- **Rol patlaması** (role explosion): istisnalar için açılan rollerin
  yönetilemeyecek kadar çoğalması.
- **Öznitelik** (attribute): karar kuralında kullanılan özellik (bölüm,
  saat, cihaz...).

## Hangisi ne zaman?

- Kişisel dosyalar, küçük ekipler: **DAC**.
- Sınıflandırılmış bilgi, sıkı kurallar: **MAC**.
- Kurum içi uygulamalar, iş tanımları belli: **RBAC**.
- Bağlama bağlı kurallar (saat, konum, ilişki): **RBAC + ABAC**.
