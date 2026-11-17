Dersteki modelde LSTM'i GRU ile değiştirmek tek satırlık iş; tek fark
GRU'nun ikinci çıkışının demet değil, doğrudan `h` olması. Aşağıdaki kod
dersteki veriyi, `train_model` ve `accuracy` fonksiyonlarını kullanıyor.

```python
class GRUClassifier(nn.Module):
    def __init__(self, vocab=10, dim=8, hidden=16):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.gru = nn.GRU(dim, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        out, h = self.gru(self.emb(x))
        return self.head(h[-1])


torch.manual_seed(0)
gru_model = train_model(GRUClassifier())
gru_acc = accuracy(gru_model, x_test, y_test)
print(sum(p.numel() for p in gru_model.parameters()))
print(round(gru_acc, 2), gru_acc > 0.9)
```

```text
1362
1.0 True
```

GRU 1362 parametreyle (LSTM'de 1778) bu görevde
de %90'ın üstünde. Kısa dizilerde ikisi çoğu zaman yakın sonuç verir;
seçim çoğunlukla hız ve bellekle ilgilidir.

## Hangisini seçmeli?

| Durum | Öneri |
|---|---|
| İlk deneme | LSTM ya da GRU, ikisini de dene; fark küçükse küçük olanı al |
| Az veri, küçük cihaz | GRU: daha az parametre, daha az aşırı öğrenme riski |
| Çok uzun bağımlılıklar | LSTM'in ayrı hücre durumu çoğu zaman biraz daha iyi |
| Çok uzun diziler, paralel hesap gerekiyor | Transformer (bu modülün dikkat bölümü) |

Bir karşılaştırma yaparken tek bir tohumla verilen karara güvenme: iki
model arasındaki küçük fark başka bir tohumla tersine dönebilir.
