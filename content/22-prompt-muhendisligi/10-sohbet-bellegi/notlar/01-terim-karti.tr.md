| Terim | Anlamı |
|---|---|
| **Durumsuz API** | Modelin önceki çağrıları hatırlamadığı, geçmişin her çağrıda gönderildiği yapı |
| **Pencere** (son N mesaj) | Geçmişin yalnızca son mesajlarını göndermek |
| **Özet** | Eski mesajların bir model çağrısıyla kısaltılmış hâli; kayıplı olabilir |
| **Bilgi belleği** | Ad, sipariş numarası gibi kesin bilgilerin yapılı olarak tutulması |
| **Uzun süreli bellek** | Bir sonraki sohbette de hatırlanan, kullanıcıya bağlı kayıt |
| **Saklama süzgeci** | Parola, kart numarası gibi bilgileri belleğe almayan denetim |

**Akılda tut:**

- Derste on mesajda bütün geçmiş 1565, son dört mesaj 695, son dört
  mesaj + bilgi belleği 847 token tuttu; sipariş numarasını yalnızca son
  dört mesaj kaybetti.
- Örnek özet dört mesajı 56 token'dan 23'e indirdi ama sipariş numarasını
  düşürdü.
- Süzgeç parola ve kart numarası içeren mesajlardan hiçbir şeyi
  saklamadı; düzenli ifadeler yine de başka yazımları kaçırabilir.
- Bellek kullanıcıya bağlı, görülebilir, silinebilir ve süreli olmalı.
