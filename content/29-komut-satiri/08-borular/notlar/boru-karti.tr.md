Borunun bütün kalıpları, bir bakışta.

## Yazımlar

| Yazım | Ne yapar |
|---|---|
| <code>a &#124; b</code> | a'nın çıktısı b'nin girdisi olur |
| <code>a &#124; b &#124; c</code> | Zincir: a → b → c |
| <code>a &#124; b &gt; f</code> | Zincirin sonucunu f'ye yazar |
| <code>a 2&gt;&amp;1 &#124; b</code> | Hata mesajlarını da b'ye verir |
| <code>a 2&gt; /dev/null &#124; b</code> | Hataları atar, yalnızca çıktıyı işler |

## Sık kullanılan zincirler

| Zincir | Ne bulur |
|---|---|
| <code>ls klasör &#124; wc -l</code> | Klasördeki öğe sayısı |
| <code>sort f &#124; head -n 3</code> | Sıralanmış ilk üç satır |
| <code>head -n 6 f &#124; tail -n 3</code> | 4., 5. ve 6. satırlar |
| <code>grep kelime f &#124; wc -l</code> | Kelimenin geçtiği satır sayısı |
| <code>cat -n f &#124; tail -n 2</code> | Son iki satır, gerçek numaralarıyla |
| <code>ls &#124; grep md</code> | Adında md geçenler |

## Borunun sağında işe yarayanlar

Girdisini okuyan komutlar: `sort`, `head`, `tail`, `wc`, `grep`, `cat`,
`uniq`, `cut`, `tr`. Girdiye bakmayanlar: `ls`, `cd`, `mkdir`, `echo`, `rm`.

## Hatırla

- Boşluk serbest: `a|b` ile `a | b` aynı.
- Kaydedeceksen `>` en sonda.
- Gerçek terminalde hem gör hem kaydet: `a | tee f`.
