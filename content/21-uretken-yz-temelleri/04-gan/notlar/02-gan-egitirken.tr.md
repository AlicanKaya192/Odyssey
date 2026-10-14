GAN eğitimi hassastır. Bölümde yalnızca öğrenme oranını 0,002'den 0,01'e
çıkarmak, üç tohumun ikisinde sekiz kümeden ikisini kaybettirdi.

**Kontrol listesi:**

1. **Üretilenlere bak.** İki boyutlu veride saçılım grafiği, resimde bir
   ızgara. Kayıp tek başına yetmez: bölümde çökmüş eğitimin son kaybı
   biraz düşüktü (sağlıklıda 1,380, çökmüşte 1,176), ama hangi kümelerin
   kaybolduğunu söylemiyordu.
2. **Türleri say.** Veride bilinen gruplar varsa (kümeler, rakamlar)
   üretilen örneklerin kaçının hangi gruba düştüğünü say. Hiç örnek
   almayan grup mod çöküşünün işaretidir.
3. **Birkaç tohum dene.** Tek bir eğitim şans eseri iyi ya da kötü
   çıkabilir; bölümde aynı ayarla bir tohum sekiz, ikisi altı küme verdi.
4. **Küçük öğrenme oranıyla başla.** Bölümde 0,002 güvenliydi. Adam'ın
   momentum katsayısı GAN'larda çoğu zaman 0,5.
5. **Ayırt ediciyi izle.** Eğitimin sonunda gerçek ve sahte örneklere
   verdiği ortalama olasılık 0,5'e yakın olmalı. Biri 1'e, öteki 0'a
   gidiyorsa ayırt edici kazanmıştır ve üretici öğrenemiyordur.

**Sık hatalar:**

- **Üreticinin adımında türevi ayırt edicinin girdisinden almamak.**
  Üretici, ayırt edicinin girdisine giden türevle güncellenir; ayırt
  edicinin kendi ağırlık türevleri burada kullanılmaz.
- **Üreticinin adımında ayırt ediciyi de güncellemek.** Her ağ yalnızca
  kendi adımında değişir.
- **Ayırt edicinin adımında sahte grubun etiketini 1 sanmak.** Sahte için
  logit türevi `p`, gerçek için `p - 1`.
- **Eski kaybı kullanmak.** $\log(1 - D(G(z)))$ başta neredeyse hiç türev
  vermez; $-\log D(G(z))$ kullan.
