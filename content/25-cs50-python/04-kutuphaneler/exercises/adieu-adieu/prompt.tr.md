*Neşeli Günler*'deki (The Sound of Music) *So Long, Farewell* şarkısında çocuklar sırayla vedalaşır; "adieu" Fransızca "hoşça kal".

Kullanıcı girdiyi bitirene kadar (`Ctrl+D`, `EOFError`) satır satır isim isteyen bir program yaz; en az bir isim geleceğini varsay. Sonra o isimlere veda et: iki ismi bir `and` ile, üç ismi iki virgül ve bir `and` ile, `n` ismi `n - 1` virgül ve bir `and` ile birleştir:

- `Adieu, adieu, to Liesl`
- `Adieu, adieu, to Liesl and Friedrich`
- `Adieu, adieu, to Liesl, Friedrich, and Louisa`

(CS50'de dosyanın adı `adieu.py`.)

İpucu (CS50'den): `inflect` paketi bunu yapar: `p = inflect.engine()`, `p.join(names)`.

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `Liesl` → çıktı `Adieu, adieu, to Liesl`
- Girdi `Liesl`, `Friedrich` → çıktı `Adieu, adieu, to Liesl and Friedrich`
- Girdi `Liesl`, `Friedrich`, `Louisa` → çıktı `Adieu, adieu, to Liesl, Friedrich, and Louisa`
- Girdi `Liesl`, `Friedrich`, `Louisa`, `Kurt`, `Brigitta`, `Marta`, `Gretl` → çıktı `Adieu, adieu, to Liesl, Friedrich, Louisa, Kurt, Brigitta, Marta, and Gretl`
