Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Yazılış

| Kavram | Anlamı |
|---|---|
| $A\mathbf{x} = \mathbf{b}$ | Katsayı matrisi, bilinmeyenler, sağ taraf |
| $[A \mid \mathbf{b}]$ | Artırılmış matris: her satır bir denklem |
| $R_i$ | $i$. satır |
| Pivot | Basamak biçiminde bir satırın ilk sıfır olmayan elemanı |
| Serbest değişken | Pivotu olmayan sütunun bilinmeyeni |

## Satır işlemleri (çözümü değiştirmez)

| İşlem | Determinanta etkisi |
|---|---|
| $R_i \leftrightarrow R_j$ | işaret değişir |
| $R_i \to c\,R_i$, $c \ne 0$ | $c$ ile çarpılır |
| $R_i \to R_i + c\,R_j$ | değişmez |

Her işlem satırın **tamamına**, sağ taraf dahil uygulanır.

## Gauss eleme

1. Sütun sütun ilerle; pivot sıfırsa alttaki bir satırla yer değiştir.
2. Pivotun altındaki her satır için $R_i \to R_i - \dfrac{a_{i\,k}}{\text{pivot}}\,R_k$.
3. Basamak biçimine gelince en alttan başlayıp **geri yerine koy**.
4. Bulduğun çözümü **orijinal** denklemlerde sına.

## Sonucu okumak

| Eleme sonunda | Çözüm |
|---|---|
| Her bilinmeyenin sütununda pivot var | tek |
| $[\,0 \;\cdots\; 0 \mid c\,]$, $c \ne 0$ | yok (tutarsız) |
| $0 = c$ yok, pivotsuz sütun var | sonsuz; serbest değişken $= t$ |

Doğrusal bir sistemin çözüm sayısı **yalnızca** 0, 1 ya da sonsuz olabilir.

Kare sistemde: $\det A \ne 0 \iff$ tek çözüm.

## Gauss–Jordan

- Pivotları $1$ yap, pivotların hem altını hem üstünü sıfırla.
- Çözüm son sütunda doğrudan okunur.
- Ters: $[A \mid I] \to [I \mid A^{-1}]$. Sol taraf $I$ olmuyorsa ters yok.

## Elemeyle determinant

$$
\det A = (-1)^{\text{yer değiştirme sayısı}} \cdot (\text{pivotların çarpımı})
$$

(yalnızca ekleme ve yer değiştirme kullanıldıysa)

## Hesap maliyeti

| Yöntem | $n \times n$ için yaklaşık iş |
|---|---|
| Gauss eleme | $n^3 / 3$ |
| Ters alıp çarpmak | $n^3$ |
| Determinantı açılımla | $n!$ |

## Pratik ipuçları

- İlk satıra pivotu $1$ olan denklemi al (gerekirse yer değiştir); kesirsiz ilerlersin.
- Her adımda hangi işlemi yaptığını ($R_2 - 2R_1$ gibi) yanına yaz.
- Kesirlerden kaçmak için bir satırı önce bir tam sayıyla çarpabilirsin.
- Sonsuz çözümde cevabı parametreyle yaz: $(-1 + t,\ 3 - 2t,\ t)$.
