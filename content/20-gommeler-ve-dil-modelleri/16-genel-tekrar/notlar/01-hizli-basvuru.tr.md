## Gömmeler

| Yazım | Ne |
|---|---|
| `M[a, b] += 1` pencere içinde | birlikte geçme sayımı |
| `np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))` | PMI |
| `np.maximum(P, 0)` | PPMI |
| `U, S, _ = np.linalg.svd(P)`; `U[:, :k] * S[:k]` | kesik SVD ile vektörler |
| `E / np.linalg.norm(E, axis=1, keepdims=True)` | birim vektör; nokta çarpımı = kosinüs |
| `E[a] - E[b] + E[c]` | benzetme |
| `np.mean(E[ids], axis=0)` | belge vektörü |

## Alt kelime ve dil modeli

| Yazım | Ne |
|---|---|
| en sık bitişik çifti birleştir | BPE'nin bir adımı |
| `(sayı(a, b) + k) / (sayı(a) + k · V)` | toplamalı yumuşatma |
| `exp(−ortalama log p)` | karmaşıklık (perplexity) |
| `λ · p_trigram + (1 − λ) · p_bigram` | ara değer |
| `skor[t, j] = max_i(skor[t-1, i] + log geçiş) + log yayılım` | Viterbi |

## Sinir ağları

| Yazım | Ne |
|---|---|
| `np.exp(z - z.max())` ve satır toplamına böl | kararlı softmax |
| `p − y` | softmax + çapraz entropinin türevi |
| `(kayıp(w + ε) − kayıp(w − ε)) / 2ε` | türev denetimi |
| `h = tanh(x Wx + h Wh + b)` | RNN adımı |
| `min(1, sınır / norm)` | türev kırpma |
| `softmax(Q @ K.T / √d) @ V` | ölçekli nokta çarpım dikkati |
| `a · (da − a · da)` | softmax'ın geri hesabı |
| `np.tril(np.ones((n, n), dtype=bool))` | nedensel maske |
| `X + f(norm(X))` | artık bağlantı (girişte norm) |

## Kullanmak ve ölçmek

| Yazım | Ne |
|---|---|
| ön eğitimli vektör + küçük sınıflandırıcı | öznitelik çıkarmak |
| kategori anlatımına benzerlik | sıfır atışlı sınıflandırma |
| `p ** (1 / T)` | sıcaklık |
| en olası k; toplamı p'ye ulaşan küme | top-k, top-p |
| kırpılmış n-gram kesinliği × kısalık cezası | BLEU |
| referans n-gram'larının geri çağırması; LCS | ROUGE-N, ROUGE-L |
| `(p_o − p_e) / (1 − p_e)` | Cohen'in kappa'sı |
| `1 / ilk doğru sıra` ortalaması | MRR |

## Sık yapılan hatalar

| Hata | Bu modülde |
|---|---|
| Ham sayımlarla vektör kurmak | PPMI ve SVD ile Kelime Vektörleri |
| Öğrenme oranını büyük seçmek (`nan`) | Word2Vec |
| Gömmelerdeki önyargıyı yok saymak | Gömmelerle Çalışmak |
| Yumuşatmasız dil modeli | n-gram Dil Modeli |
| Ağırlıkları sıfırla başlatmak | Sinir Ağıyla Metin Sınıflandırma |
| Dikkat ağırlığını açıklama sanmak | Dikkat Mekanizması |
| Yanlış alandan ön eğitim | Önceden Eğitilmiş Modeller |
| BLEU'yu anlam ölçüsü sanmak | NLP'de Değerlendirme |
| Eşiği sınav kümesinde seçmek | Bitirme: Anlamsal Arama Motoru |
