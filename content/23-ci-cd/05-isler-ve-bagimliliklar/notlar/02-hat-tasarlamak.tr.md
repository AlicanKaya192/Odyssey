**Bir hattı tasarlarken sorulacaklar**

1. **Hangi işler birbirinden bağımsız?** Bağımsız olanlar aynı anda
   çalışsın: lint, testler, belge derlemesi.
2. **Neyin neyi beklemesi gerekiyor?** Yalnızca gerçekten gerekenlere
   `needs` yaz. Gereksiz `needs` hattı uzatır.
3. **Kritik yol hangisi?** Hattın süresini o belirler; hızlandırma işi
   oradan başlar.
4. **Ne yalnızca `main`'de olmalı?** Dağıtım, sürüm, yayın → `if`.
5. **Bir şey düşünce kim haber alacak?** `if: failure()` ile bildirim.

**Hızlı olan önce**

Kısa süren denetimleri (lint, biçim) ayrı bir iş yap ve uzun işler
onları beklesin ya da yanlarında çalışsın. Bir yazım hatası için altı
dakikalık testi beklemek gerekmez; lint bir dakikada söyler.

**Sık hatalar**

| Yazılan | Sonuç | Doğrusu |
|---|---|---|
| `needs: tests` (iş adı `test`) | Dosya geçersiz | İş adını aynen yaz |
| `a` → `b`, `b` → `a` | Döngü, dosya geçersiz | Bir ok kaldırılır |
| `if: github.ref == "refs/heads/main"` | İfadede çift tırnak hata verir | Tek tırnak: `'refs/heads/main'` |
| `notify`'da `if: failure()` yok | Bir şey düşünce çalışmaz (atlanır) | `if: failure()` |
| Dağıtımda `if` yok | PR'larda da dağıtım denenir | `github.event_name == 'push' && github.ref == 'refs/heads/main'` |
| Bir işin dosyasını öbüründe aramak | Dosya yok: ayrı makine | Artifact (sekizinci bölüm) |

**Dalgalar ve süre** (dersteki örnek)

| Dalga | İşler | Biter |
|---|---|---|
| 1 | `lint` (1), `test` (6), `docs` (2) | 6. dakika |
| 2 | `build` (3) | 9. dakika |
| 3 | `deploy` (2) | 11. dakika |

Sırayla çalışsaydı 14 dakika.
