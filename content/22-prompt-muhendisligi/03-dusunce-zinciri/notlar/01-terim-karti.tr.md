| Terim | Anlamı |
|---|---|
| **Adım adım düşündürmek** (chain-of-thought) | Modelden cevaptan önce ara adımları yazmasını istemek |
| **Son cevap satırı** | Adımlı cevapta programın ayrıştırdığı sabit satır (`Answer: ...`) |
| **Hesap hatası** | Yazılan işlemin sonucunun yanlış olması (`214.90 * 0.10 = 21.94`) |
| **Akıl yürütme hatası** | İşlemler doğru ama adım yanlış ya da eksik (bir çifti unutmak) |
| **Çoğunluk oyu** | Aynı soruyu birkaç kez sorup en sık gelen son cevabı almak |
| **Kesin hesap** | Para, tarih, birim çevirme gibi tek doğru sonucu olan ve kodla yapılabilen hesap |

**Akılda tut:**

- Derste dört örnek yanıttan yalnızca biri doğru tutarı verdi; kod
  unutulan adımı, hesap hatasını ve eksik son satırı ayırdı.
- Adım denetleyicisi yalnızca hesap hatasını buldu; doğru hesaplanmış
  yanlış adımı göremedi.
- Adımlı cevap doğrudan cevabın 10 katı token tuttu;
  çoğunluk oyu çağrı sayısını da katlar.
- Müşteriye çoğu zaman yalnızca son cevap gösterilir.
