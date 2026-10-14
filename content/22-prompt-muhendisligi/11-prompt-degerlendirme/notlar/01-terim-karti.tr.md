| Terim | Anlamı |
|---|---|
| **Değerlendirme kümesi** | Doğru cevabı bilinen girdiler; her prompt sürümü aynı kümede puanlanır |
| **Birebir doğru** (exact) | Cevabın hiçbir temizlik yapılmadan doğru etikete eşit olması |
| **Geçerli** (valid) | Cevabın programın ayrıştırabileceği biçimde olması |
| **Doğru** (right) | Ayrıştırılan değerin doğru etiket olması |
| **Karışan çift** | En sık birbiriyle karışan iki kategori |
| **Puanlayan model** (model as a judge) | Açık uçlu cevapları bir ölçütle puanlayan ayrı bir model çağrısı |
| **Gerileme** (regression) | Bir düzeltmenin başka bir yeri bozması |

**Akılda tut:**

- Derste `v1` ve `v2`'nin cevapları ders için yazılmış örnek yanıtlardı;
  sayılar bir modelin ölçümü değil, puanlama yönteminin gösterimi.
- `v1`: birebir 26, geçerli 36, doğru 31; `v2`: 35, 39, 36 (40 mesajda).
- İki sürümde de en çok karışan çift para iadesi ↔ ödeme.
- Fark 0,125 ama yeniden örneklemenin %90 aralığı 0 ile 0,25 arasında:
  kırk mesajda beş mesajlık fark bile kesin değil.
