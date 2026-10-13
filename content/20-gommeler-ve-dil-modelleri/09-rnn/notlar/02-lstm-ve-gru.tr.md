Düz RNN'de gizli durum her adımda baştan hesaplanır: eski bilgi `W_h` ile
çarpılıp `tanh`'tan geçer. **LSTM** (long short-term memory, uzun kısa süreli
bellek; Hochreiter ve Schmidhuber, 1997) yanına ayrı bir **hücre durumu**
(cell state) ekler ve onu çarpmayla değil **toplamayla** günceller:

$$c_t = f_t \cdot c_{t-1} + i_t \cdot g_t$$

- `f` (forget, unutma kapısı) eskinin ne kadarının kalacağını,
- `i` (input, yazma kapısı) yeni bilginin (`g`) ne kadar yazılacağını,
- üçüncü bir `o` (output) kapısı hücreden ne kadarının gizli duruma
  çıkacağını söyler. Kapılar 0 ile 1 arasında, sigmoid ile hesaplanır ve
  ağın kendisi tarafından öğrenilir.

Kapılar sabitken ne olduğunu sayılarla görelim:

```python
def lstm_cell(c, forget, write, new):
    return forget * c + write * new


c = 1.0
for step in range(50):
    c = lstm_cell(c, forget=0.99, write=0.0, new=0.0)
h = 1.0
for step in range(50):
    h = 0.9 * h
print(round(h, 4), round(c, 4))
c = lstm_cell(c, forget=0.0, write=1.0, new=-1.0)
print(c)
```

```text
0.0052 0.605
-1.0
```

- Her adımda 0,9 ile çarpılan bilgi 50 adımda 0,0052'ye iniyor; unutma
  kapısı 0,99'da açık duran hücre 0,605'ini koruyor. Hücre üzerinden geriye
  giden türev de aynı çarpanlardan geçer (`f` değerleri), bu yüzden
  kaybolmaz.
- Unutma kapısı 0 ve yazma kapısı 1 olunca hücre eskiyi tamamen silip yeni
  değeri yazıyor. Model neyi ne zaman unutacağını öğrenir: yeni bir cümlenin
  öznesi gelince eskisini silmek gibi.
- **GRU** (gated recurrent unit, 2014) aynı fikrin sadeleşmiş hâli: iki kapı,
  ayrı hücre durumu yok. Çoğu görevde LSTM'e yakın sonuç verir, daha az
  parametreyle.
- LSTM 2010'ların ortasına kadar makine çevirisinde ve konuşma tanımada
  standarttı. Bugün büyük dil modelleri dikkat mekanizmasıyla kuruluyor;
  sebebi sonraki iki bölümde.
