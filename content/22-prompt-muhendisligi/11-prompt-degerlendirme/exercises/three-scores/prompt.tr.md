`scores(replies, gold, labels)` cevapları doğru etiketlerle karşılaştırıp
`[birebir, geçerli, doğru]` döndürsün: birebir, cevabın hiçbir temizlik
yapılmadan doğru etikete eşit olduğu sayı; geçerli, temizlenmiş cevabın
(`strip`, `lower`, sondaki `.` ve `!` atılmış) `labels`'ta olduğu sayı;
doğru, temizlenmiş cevabın doğru etikete eşit olduğu sayı.

**Beklenen çıktı:**

```
[1, 3, 2]
```
