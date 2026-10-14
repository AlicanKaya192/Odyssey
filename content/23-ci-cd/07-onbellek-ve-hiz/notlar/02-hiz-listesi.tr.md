**Önce ölç**

GitHub'da çalışmanın içinde her adımın süresi yazar. En uzun adımı bul;
hızlandırma oradan başlar. Hattın toplam süresini kritik yol belirler
(beşinci bölüm): kritik yolda olmayan bir işi hızlandırmak hattı
kısaltmaz.

**Kontrol listesi**

| Soru | Yol | Bölüm |
|---|---|---|
| Bağımlılıklar her seferinde mi iniyor? | `cache: pip` ya da `actions/cache` | 7 |
| Belge değişikliği testleri çalıştırıyor mu? | `paths-ignore` | 4 |
| Aynı dalda eski çalışmalar sürüyor mu? | `concurrency` + `cancel-in-progress` | 7 |
| PR'da testler iki kez mi çalışıyor? | `push`'u `main` ile sınırla | 4 |
| Bağımsız işler sırayla mı? | Gereksiz `needs`'i kaldır | 5 |
| Hızlı denetim uzun testi mi bekliyor? | Lint ayrı iş | 5 |
| Matris gereğinden büyük mü? | `exclude`, sistemleri tek sürümle | 6 |
| Hatalı PR'da bütün testler mi bekleniyor? | `pytest -x` | 7 |
| Takılan iş saatlerce mi sürüyor? | `timeout-minutes` | 3, 7 |

**Tuzaklar**

- Anahtarda `hashFiles` yok → bağımlılık değişse de eski paketler geri
  gelir.
- Anahtarda `runner.os` yok → Windows paketi Linux'a yüklenir.
- Önbellek adımı kurulumdan sonra → geri yükleme işe yaramaz.
- Dağıtımda `cancel-in-progress: true` → yarım kalmış dağıtım.
- Hız için testleri silmek ya da atlamak → hat hızlı ama hiçbir şey
  yakalamıyor.
