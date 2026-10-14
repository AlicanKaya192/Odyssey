`few_shot_messages(system, examples, question)` bir mesaj listesi kursun:
önce `system` rolünde `system`; sonra her `[metin, etiket]` örneği için
`user` rolünde metin ve `assistant` rolünde etiket; en sonda `user`
rolünde `question`.

**Beklenen çıktı:**

```
system | Classify.
user | Where is my parcel?
assistant | shipping
user | My card was declined.
assistant | payment
user | Refund?
```
