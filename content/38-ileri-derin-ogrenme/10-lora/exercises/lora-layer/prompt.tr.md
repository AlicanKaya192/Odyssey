`LoRALinear` sınıfını tamamla: `A` (`r × giriş`, küçük rastgele sayılar,
`torch.randn(...) * 0.01`), `B` (`çıkış × r`, sıfır) parametreleri ve
`scale = alpha / r`; `forward` taban çıkışına `(x · Aᵀ · Bᵀ) · scale` eklesin.
`lora_report` hazır: başlangıçta çıkış tabanla aynı mı, kaç sayı eğitiliyor,
`B` doldurulunca çıkış değişiyor mu.

**Beklenen çıktı:**

```
[True, 24, True]
```
