| Terim | Anlamı |
|---|---|
| **Sıfır örnekli prompt** (zero-shot) | Yalnızca talimat veren prompt |
| **Az örnekli prompt** (few-shot) | Talimata birkaç çözülmüş örnek ekleyen prompt |
| **Örnek** (shot) | Bir girdi ve onun doğru cevabı |
| **Örnek havuzu** | Prompt'a konacak örneklerin seçildiği etiketli mesajlar |
| **Test kümesi** | Prompt'u sınamak için ayrılan, örnek olarak kullanılmayan mesajlar |
| **Dengeli seçim** | Her kategoriden aynı sayıda örnek alıp karıştırmak |
| **Benzerliğe göre seçim** | Her yeni girdi için ona en çok benzeyen örnekleri seçmek |
| **Sızıntı** (leakage) | Test mesajının örnek olarak prompt'a girmesi; başarıyı olduğundan iyi gösterir |

**Akılda tut:**

- Örnekler her çağrıda yeniden gönderilir: derste on örnek, sıfır
  örnekli prompt'un 5,1 katı token tuttu.
- Rastgele beş örnek, bin çekilişin 932'sinde en az bir
  kategoriyi kaçırdı.
- TF-IDF ile en benzer örnek, on test mesajının 6'sında aynı
  kategorideydi; kelime örtüşmesi zayıf bir benzerlik ölçüsü.
- Örnek cevaplar tam istenen biçimde yazılır; model biçimi örnekten
  öğrenir.
