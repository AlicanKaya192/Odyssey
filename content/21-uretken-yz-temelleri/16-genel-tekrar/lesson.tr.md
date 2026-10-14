# Genel Tekrar

Üretken YZ Temelleri modülünün sonuna geldin. Bir dağılımdan örnek
çekmekle başladık; otomatik kodlayıcı, VAE, GAN ve difüzyonla resim ve nokta
ürettik. Sonra büyük dil modellerine geçtik: nasıl ürettiklerini, token ve
maliyeti, halüsinasyonu ölçtük; belgeleri parçalayıp aradık, RAG kurduk ve
değerlendirdik; ince ayarı, hizalamayı ve LoRA'yı denedik; önyargıyı ve
kişisel veriyi ölçtük ve bir belge soru-cevap sistemi kurduk. Bu bölüm yolu
bir kez daha yürüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Üretken modeller<br><small>00–05</small></span><span class="arrow">→</span>
    <span class="node">Dil modelleri<br><small>06–08</small></span><span class="arrow">→</span>
    <span class="node">RAG<br><small>09–11</small></span><span class="arrow">→</span>
    <span class="node">Uyarlama<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Sorumluluk ve proje<br><small>14–15</small></span>
  </div>
  <figcaption>Modülün yolu: dağılımdan örnek üret, dil modelini anla, belgelere dayandır, modeli uyarla, sorumlu bir sistem kur.</figcaption>
</figure>

## 1. Üretken modeller (Bölüm 0–5)

- **Üretken model** verinin dağılımını öğrenir ve ondan yeni örnek çeker;
  ezberi en yakın komşu uzaklığıyla denetleriz (00).
- **Örnekleme:** olasılık cetveli, ters dönüşüm, reddetme yöntemi (01).
- **Otomatik kodlayıcı** sıkıştırır ama kod uzayı düzensizdir: rastgele
  koddan net rakam %32 (02).
- **VAE** kodu standart normale çeker: oradan çekilen kodlarla 10 rakamın
  hepsi çıktı (03).
- **GAN** keskin ama kırılgan: öğrenme oranı 0,01'de iki tohumda iki küme
  kayboldu (04).
- **Difüzyon** gürültüyü geri almayı öğrenir: aynı ayarda üç tohumda sekiz
  küme; bedeli 100 adımlık üretim (05).

## 2. Büyük dil modelleri (Bölüm 6–8)

- Model yalnızca devam ettirir; sohbet bir **şablondur**. Bitiş nedeni
  `stop` ya da `length` (06).
- Geçmiş her çağrıda yeniden gönderilir: sekiz mesajda toplam giren token
  son çağrının 4,5 katı; **maliyet** giren ve çıkan token'la hesaplanır (07).
- **Halüsinasyon:** model bilmediğine de akıcı cevap verir. Öz tutarlılık
  ve kaynak denetimi onu yakalamaya yardım eder (08).

## 3. RAG (Bölüm 9–11)

- Belgeler **parçalanır**, soruya en yakın parçalar **vektör aramayla**
  bulunur; parça boyu bir ödünleşimdir (09).
- **RAG:** parçalar numaralanıp prompt'a konur, cevap kaynağa dayanır,
  bulunamazsa "bulamadım" denir (10).
- **Değerlendirme:** getirme (recall@k, MRR), cevap ve çekimser kalma ayrı
  ölçülür; hataların çoğu getirmedeydi (11).

## 4. Uyarlama (Bölüm 12–13)

- **İnce ayar** eskiyi unutturabilir; eski veriyi karıştırmak korur.
  **Ödül modeli** tercihlerden öğrenir, yanlılıklarını da (12).
- **LoRA** değişimi düşük ranklı iki matrisle yazar: 714 parametreyle tam
  ince ayar düzeyi (13).

## 5. Sorumluluk ve proje (Bölüm 14–15)

- **Önyargı** veriden gelir; grup sütununu silmek vekil değişken yüzünden
  yetmez. **Kişisel veri** maskelenir ve maskeleyici ölçülür (14).
- **Belge soru-cevap sistemi:** maskele → ara → bütçeye sığdır → prompt →
  cevap → doğrula → kaydet → ölç (15).

## Hepsi birlikte: RAG neden var?

Bütün yardım makalelerini her soruda modele göndersek ne olurdu? Token
sayısını 09'daki aramayla karşılaştıralım:

```python
from retrieval import Index, by_sentence, QUESTIONS, DOCS, count_tokens

everything = sum(count_tokens(d["title"] + " " + d["text"]) for d in DOCS)
index = Index(by_sentence())
rag_tokens = [sum(count_tokens(text) for (_, text), _ in
                  index.search(q["q"], 3)) for q in QUESTIONS]
average = sum(rag_tokens) / len(rag_tokens)
print("all articles", everything, "tokens per question")
print(f"RAG, 3 sentences {average:.0f} tokens per question")
print(f"ratio {everything / average:.1f}")
```

```text
all articles 979 tokens per question
RAG, 3 sentences 50 tokens per question
ratio 19.7
```

Bütün makaleleri göndermek soru başına 979 token; RAG ile seçilen 3 cümle
ortalama 50 token, yaklaşık 20 kat az. Bu küçük mağazanın 14 kısa makalesi
bile her soruda bin token'a yaklaşıyor; bir şirketin binlerce sayfası
hiçbir bağlam penceresine sığmaz. RAG'in bedeli ise 10 ve 11'de gördüğümüz
kaçırmalar ve yanlış getirme; bu yüzden arama da cevap da ayrı ayrı
ölçülür.

## Sonra

Bir sonraki modül, **Prompt Mühendisliği ve LLM Uygulamaları**, modelle
konuşmanın kendisine odaklanıyor: net talimat, örnekli prompt, adım adım
düşündürmek, yapılı çıktı, araç çağırma, ajan döngüsü, sohbet
belleği, prompt injection'a karşı savunma ve promptları ölçerek
iyileştirmek. Burada kurduğun parçalar (istemci, token sayımı, RAG,
doğrulama, değerlendirme) orada da kullanılacak.
