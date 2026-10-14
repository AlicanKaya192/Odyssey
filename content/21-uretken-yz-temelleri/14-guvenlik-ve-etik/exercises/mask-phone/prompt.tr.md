Dersteki maskeleyici `(555) 123-4567` biçiminde ilk parantezi dışarıda
bırakıyordu. `mask(text)` e-posta, telefon ve sipariş numarasını dersteki gibi
`[EMAIL]`, `[PHONE]`, `[ORDER]` ile değiştirsin; ama telefon deseni baştaki
isteğe bağlı `(` işaretini de kapsasın: `r"\+?\(?\d[\d\s()-]{8,}\d"`.

**Beklenen çıktı:**

```
My number is [PHONE].
Mail [EMAIL]
Order [ORDER]
```
