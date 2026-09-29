"""Belge alanlarının stili.

Konu anlatımı, ders notları ve alıştırma yönergesi `QWebEngineView` ile
çiziliyor. O motor Chromium olduğu için maketteki CSS burada birebir
çalışıyor — Qt'nin kendi metin motorunda desteklenmeyen yuvarlak köşe,
gölge, kod renklendirmesi ve yazı tipi ağırlıkları dahil.

Kurallar `Plan/tasarim/maket.html` dosyasındaki `.content` bloğuyla aynı
tutuluyor. Renkler ve ölçüler `tokens.py`'den geliyor, elle yazılmıyor.
"""

from __future__ import annotations

from .tokens import FONTS, PALETTES, READING_WIDTH, SYNTAX, TOC_WIDTH


def build_css(mode: str) -> str:
    """Belge stilini seçili temaya göre üretir."""
    p = PALETTES.get(mode, PALETTES["light"])
    s = SYNTAX.get(mode, SYNTAX["light"])

    return f"""
/* Kod renkleri sınıfla veriliyor, satır içi renkle değil. Böylece tema
 * değişince belgeyi baştan yüklemek gerekmiyor; yalnızca bu stil bloğu
 * değiştiriliyor. */
.hl-keyword  {{ color: {s['keyword']}; font-weight: 600; }}
.hl-constant {{ color: {s['constant']}; font-weight: 600; }}
.hl-builtin  {{ color: {s['builtin']}; }}
.hl-string   {{ color: {s['string']}; }}
.hl-number   {{ color: {s['number']}; }}
.hl-comment  {{ color: {s['comment']}; font-style: italic; }}
.hl-variable {{ color: {s['variable']}; }}
.hl-definition {{ color: {s['definition']}; }}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{ scroll-behavior: smooth; }}

body {{
    background: {p['bg']};
    color: {p['text']};
    font-family: {FONTS['ui']};
    font-size: 15px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}}

::-webkit-scrollbar {{ width: 12px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {p['border_strong']};
    border-radius: 6px;
    border: 3px solid {p['bg']};
}}
::-webkit-scrollbar-thumb:hover {{ background: {p['text_muted']}; }}

/* --- sayfa düzeni: metin ortada, başlık listesi sağda --------------- */

.page {{
    display: grid;
    grid-template-columns: 1fr minmax(0, {READING_WIDTH}px) {TOC_WIDTH}px 1fr;
    padding: 40px 36px 90px;
    gap: 0;
}}

.page.narrow {{
    grid-template-columns: 1fr minmax(0, {READING_WIDTH}px) 1fr;
    padding: 40px 44px 80px;
}}

.page.compact {{
    display: block;
    padding: 24px 20px 40px;
}}

.content {{ grid-column: 2; min-width: 0; }}
.page.narrow .content {{ grid-column: 2; }}
.page.compact .content {{ grid-column: auto; }}

aside.toc {{ grid-column: 3; padding-left: 48px; }}

/* Sayfa kayarken başlık listesi yerinde kalsın; asıl derdi bu çözüyor. */
.toc-inner {{ position: sticky; top: 24px; }}

.toc-inner .h {{
    font-size: 11.5px; font-weight: 750; letter-spacing: 1px;
    text-transform: uppercase; color: {p['text_muted']}; margin-bottom: 14px;
}}
.toc-inner a {{
    display: block; font-size: 13.5px; color: {p['text_muted']};
    text-decoration: none; padding: 7px 0 7px 14px;
    border-left: 2px solid {p['border']}; line-height: 1.45;
}}
.toc-inner a.on {{ color: {p['accent']}; font-weight: 600; }}
.toc-links {{ position: relative; }}
.toc-links a {{ transition: color 120ms var(--out); }}
/* Seçili başlığın işareti: kenar çizgisinin üstünde yayla kayar (C5). */
.toc-mark {{
    position: absolute; left: 0; top: 0; width: 2px; height: 0; border-radius: 2px;
    background: {p['accent']};
    transition: transform 360ms var(--spring), height 360ms var(--spring);
}}
.content pre {{ position: relative; }}
.content pre .cp {{
    position: absolute; right: 10px; top: 10px; width: 30px; height: 30px; border: 0;
    border-radius: 8px; background: transparent; color: {p['text_muted']}; cursor: pointer;
    display: grid; place-items: center; opacity: 0; transition: opacity 180ms var(--out), background 120ms;
}}
.content pre:hover .cp {{ opacity: 1; }}
.content pre .cp:hover {{ background: {p['surface_hover']}; color: {p['text']}; }}
.content pre .cp.done {{ opacity: 1; color: {p['success']}; }}
.toc-inner a:hover {{ color: {p['text']}; }}

/* Bölüm ilerlemesi (prototip `.progcard`): üç adım, bitenin dairesi yeşil. */
.prog {{
    margin-top: 22px; padding: 16px;
    background: {p['surface']}; border: 1px solid {p['border']}; border-radius: 18px;
    box-shadow: 0 6px 24px rgba(0, 0, 0, {'.35' if mode == 'dark' else '.07'});
}}
.prog .h2 {{ font-size: 13px; font-weight: 600; color: {p['text_muted']}; margin-bottom: 12px; }}
.steps3 {{ display: flex; flex-direction: column; gap: 10px; }}
.step3 {{ display: flex; align-items: center; gap: 10px; font-size: 13px; color: {p['text']}; }}
.step3 .o {{
    width: 22px; height: 22px; border-radius: 50%; box-sizing: border-box;
    border: 2px solid {p['border_strong']}; display: grid; place-items: center; flex: none;
    transition: background 180ms var(--out), border-color 180ms var(--out);
}}
.step3.done .o {{ background: {p['success']}; border-color: {p['success']}; color: #fff; }}
.step3 .o svg {{ width: 13px; height: 13px; display: none; }}
.step3.done .o svg {{ display: block; animation: pop 560ms var(--bounce); }}
.step3 small {{ margin-left: auto; font-size: 12px; color: {p['text_muted']}; }}
.bar {{ height: 7px; background: {p['border']}; border-radius: 4px; overflow: hidden; }}
.bar i {{ display: block; height: 100%; background: {p['accent']}; border-radius: 4px; }}

/* --- metin ---------------------------------------------------------- */

.content h1 {{
    font-family: {FONTS['display']};
    font-size: 34px; font-weight: 700; letter-spacing: -.3px;
    margin-bottom: 10px; color: {p['text']};
}}
.content h2 {{
    font-family: {FONTS['display']};
    font-size: 21px; font-weight: 700; margin: 36px 0 12px;
    letter-spacing: -.2px; color: {p['text']};
}}
.content h3 {{
    font-size: 17px; font-weight: 650; margin: 26px 0 10px; color: {p['text']};
}}
.content p {{ margin: 14px 0; color: {p['text']}; }}
.content ul, .content ol {{ margin: 12px 0 12px 22px; }}
.content li {{ margin: 7px 0; }}
.content a {{ color: {p['accent']}; }}
.content strong {{ font-weight: 650; }}
.content hr {{ border: none; border-top: 1px solid {p['border']}; margin: 32px 0; }}

.meta {{
    color: {p['text_muted']}; font-size: 13.5px;
    margin-bottom: 30px; display: flex; gap: 16px; flex-wrap: wrap;
}}

/* --- kod ------------------------------------------------------------ */

.content code {{
    font-family: {FONTS['mono']}; font-size: 13.5px;
    background: {p['code_bg']}; padding: 2px 6px;
    border-radius: 6px; color: {p['accent']};
}}
.content pre {{
    font-family: {FONTS['mono']}; font-size: 13.5px;
    background: {p['code_bg']}; border: 1px solid {p['border']};
    padding: 18px 20px; border-radius: 12px; margin: 18px 0;
    overflow-x: auto; line-height: 1.65;
}}
.content pre code {{
    background: none; padding: 0; color: {p['text']};
    border-radius: 0; font-size: 13.5px;
}}

/* Alıştırmanın "Çıktı" sekmesi: beklenen ile gelen çıktı alt alta, eş
 * aralıklı; tutmayan satır kırmızı zeminle. Tablolar hizalı kalsın diye
 * satırlar kaydırılmıyor, kutu yatay kayıyor. */
.cmp {{
    font-family: {FONTS['mono']}; font-size: 13px; line-height: 1.55;
    background: {p['code_bg']}; border: 1px solid {p['border']};
    border-radius: 12px; padding: 12px 14px; margin: 8px 0 18px;
    overflow-x: auto; white-space: pre;
}}
.cmp .ln {{ display: block; min-height: 1.55em; padding: 0 4px; border-radius: 4px; }}
.cmp .ln.diff {{ background: {p['danger_soft']}; }}
.cmp .ln.miss {{ background: {p['danger_soft']}; color: {p['text_muted']}; font-style: italic; }}
.out-label {{
    font-size: 12.5px; font-weight: 700; letter-spacing: .4px;
    color: {p['text_muted']}; margin-top: 6px;
}}
figure.fig img.out {{ display: block; max-width: 100%; height: auto; margin: 0 auto; border-radius: 8px; }}

/* --- tablo ---------------------------------------------------------- */

.content table {{
    width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;
    background: {p['surface']}; border-radius: 12px; overflow: hidden;
    box-shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
}}
.content th {{
    background: {p['surface_alt']}; text-align: left;
    padding: 12px 16px; font-weight: 640; font-size: 13px;
}}
.content td {{ padding: 12px 16px; border-top: 1px solid {p['border']}; }}

/* --- formüller (KaTeX) ---------------------------------------------- */

/* Renk metinden geliyor (KaTeX `currentColor` kullanıyor), tema kendiliğinden
 * işliyor. Uzun bir formül dar pencerede sayfayı yana taşırmasın diye kendi
 * içinde kayıyor. */
.katex {{ font-size: 1.1em; }}
.math.display {{
    margin: 20px 0; padding: 4px 0; overflow-x: auto; overflow-y: hidden;
    text-align: center;
}}
.fig .math.display {{ margin: 8px 0; }}

/* --- ipucu kutusu ve şeritler --------------------------------------- */

.content blockquote {{
    position: relative;
    background: {p['accent_soft']};
    border-left: 3px solid {p['accent']};
    border-radius: 0 12px 12px 0;
    padding: 16px 20px 16px 52px; margin: 22px 0; font-size: 14.5px;
}}
/* Ampul: ipucu kutusunun göze çarpması için. Konumlandırma ile veriliyor,
 * flex ile değil — flex olsaydı kutudaki her paragraf yan yana dizilirdi. */
.content blockquote::before {{
    content: "💡";
    position: absolute;
    left: 18px;
    top: 15px;
    font-size: 17px;
    line-height: 1.35;
}}
.content blockquote > :first-child {{ margin-top: 0; }}
.content blockquote > :last-child {{ margin-bottom: 0; }}
.content blockquote p {{ margin: 0 0 8px; }}
.content blockquote pre {{ margin: 10px 0; }}

/* Notlarım: kullanıcının alıntısı bir ipucu değil, ampul çizilmiyor. */
.notebook .content blockquote {{ padding-left: 20px; }}
.notebook .content blockquote::before {{ content: none; }}

.banner {{
    border-radius: 12px; padding: 13px 18px; margin-bottom: 26px;
    font-size: 14px; display: flex; gap: 11px; align-items: flex-start;
}}
.banner.warn {{
    background: {p['warning_soft']}; border: 1px solid {p['warning']};
    color: {p['warning']};
}}
.banner.ok {{
    background: {p['success_soft']}; border: 1px solid {p['success']};
    color: {p['success']};
}}

/* --- ders görselleri -------------------------------------------------
 *
 * Şemalar sayfanın kendi HTML'i olarak çiziliyor, dışarıdan resim
 * yüklenmiyor. Üç sebep:
 *
 * 1. **Tema.** Sayfaya gömülü şemaya buradaki renkler işliyor; açık/koyu
 *    için ayrı dosya tutmak gerekmiyor. Bir `<img>` ayrı bir belge olduğu
 *    için sayfanın stilini alamazdı.
 * 2. **Çeviri.** Etiketler doğrudan `lesson.tr.md` / `lesson.en.md`
 *    içinde duruyor; çevirmek için görsel düzenlemek gerekmiyor.
 * 3. **Ölçek.** Metinle aynı yazı tipinde büyüyüp küçülüyor, bulanmıyor.
 *
 * Markdown tarafında iki tuzak var, ikisi de ölçüldü:
 *
 * - Blok HTML'in **içi markdown olarak işlenmiyor.** `<figure>` içinde
 *   `` `str` `` yazılırsa ekranda ters tırnaklarla görünür; oraya
 *   `<code>str</code>` yazılmalı.
 * - Çıplak `<svg>` `<p>` içine sarılıyor, çünkü markdown `svg`'yi blok
 *   etiketi saymıyor. Her görsel `<figure class="fig">` ile sarılıyor.
 */

figure.fig {{
    margin: 26px 0;
    padding: 20px 20px 14px;
    background: {p['surface']};
    border: 1px solid {p['border']};
    border-radius: 14px;
}}
.page.compact figure.fig {{ padding: 14px 14px 10px; margin: 18px 0; }}

figure.fig figcaption {{
    margin-top: 14px;
    font-size: 13.2px;
    line-height: 1.55;
    color: {p['text_muted']};
    text-align: center;
}}

/* Elle çizilmiş şemalar için. Renkleri sayfadan alsın diye sınıfla
 * boyanıyor; `fill="#..."` yazılmıyor. */
figure.fig svg {{ display: block; max-width: 100%; height: auto; margin: 0 auto; }}
/* Yukarıdaki kural şeklin içindeki formüllere de uyuyordu: KaTeX kök
 * işaretini kendi küçük SVG'siyle çiziyor, `height: auto` onu sıfır
 * yüksekliğe indirip √ işaretini siliyordu (şekil açıklamasında görüldü). */
figure.fig .katex svg {{ max-width: none; height: inherit; margin: 0; }}
figure.fig svg .ink {{ fill: {p['text']}; }}
figure.fig svg .dim {{ fill: {p['text_muted']}; }}
figure.fig svg .box {{ fill: {p['surface_alt']}; stroke: {p['border_strong']}; }}
figure.fig svg .line {{ fill: none; stroke: {p['border_strong']}; stroke-width: 1.5; }}
/* Matematik grafikleri: ızgara, eğriler ve üstlerindeki noktalar. Eğri
 * renkleri aşağıdaki işaret renkleriyle aynı sırada. */
figure.fig svg .grid {{ stroke: {p['border']}; stroke-width: 1; }}
figure.fig svg .curve {{ fill: none; stroke: {p['accent']}; stroke-width: 2.6; stroke-linecap: round; }}
figure.fig svg .curve2 {{ fill: none; stroke: {p['warning']}; stroke-width: 2.6; stroke-linecap: round; }}
figure.fig svg .curve3 {{ fill: none; stroke: {p['text_muted']}; stroke-width: 1.5; }}
figure.fig svg .dot {{ fill: {p['accent']}; }}
figure.fig svg .dot2 {{ fill: {p['warning']}; }}
/* Üçüncü eğri / vektör (toplam vektörü gibi). Yeşil: mor ve turuncudan
 * uzak, iki temada da okunuyor. */
figure.fig svg .curve4 {{ fill: none; stroke: {p['success']}; stroke-width: 2.6; stroke-linecap: round; }}
figure.fig svg .dot3 {{ fill: {p['success']}; }}

/* Dört işaret rengi. Şemada altı çizili parça ile alttaki açıklama aynı
 * rengi taşıyor; okuyan kişi hangi açıklamanın hangi parçaya ait olduğunu
 * okla değil renkle buluyor.
 *
 * Sıra rastgele değil: renklerin **birbirinden uzak** olması gerekiyor,
 * yoksa ayırt etme işi yapılmıyor. Önce `accent` ve `accent_second` yan yana
 * konmuştu; ölçüldü, açık temada aralarındaki fark ΔE 14 çıktı (25'in altı
 * "zor ayırt edilir" sayılıyor) ve koyu temada ikisi de mor görünüyordu.
 * Şimdiki sırada en yakın iki renk arasında ΔE 80 var.
 *
 * Renk tek ipucu değil: açıklama metni ve altı çizili parçanın konumu da
 * eşleştiriyor. */
.fig .m1 {{ --im: {p['accent']}; }}
.fig .m2 {{ --im: {p['warning']}; }}
.fig .m3 {{ --im: {p['success']}; }}
.fig .m4 {{ --im: {p['accent_second']}; }}

/* Kod anatomisi: bir satır kodun parçalarını adlandırır. */
.anat .sig {{
    font-family: {FONTS['mono']};
    font-size: 14.5px;
    line-height: 2.1;
    background: {p['code_bg']};
    border: 1px solid {p['border']};
    border-radius: 10px;
    padding: 14px 18px;
    overflow-x: auto;
    white-space: pre;
    color: {p['text']};
}}
.anat .sig u {{
    text-decoration: none;
    padding-bottom: 2px;
    border-bottom: 2.5px solid var(--im);
}}
.anat .legend {{ list-style: none; margin: 16px 0 0; padding: 0; }}
.anat .legend li {{
    position: relative;
    margin: 9px 0;
    padding-left: 22px;
    font-size: 13.8px;
    color: {p['text']};
    text-align: left;
}}
.anat .legend li::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 7px;
    width: 10px;
    height: 10px;
    border-radius: 3px;
    background: var(--im);
}}

/* Terim tablosu: solda ad, sağda açıklaması.
 *
 * `.anat .sig` / `.anat .legend` bir **kod satırının** parçalarını
 * adlandırıyor; bu ise düz bir terim listesi ve içerikte 166 satırda
 * kullanılıyor. Uzun süre karşılığı yoktu: iki span yan yana akıyor,
 * ekranda "örnek (sample)tablodaki bir satır" gibi yapışık çıkıyordu.
 *
 * Sütunlar sınıf adına değil **sıraya** göre seçiliyor; içerikte iki ad
 * birden kullanılmış (`anat-label` ve `anat-key`) ve ikinci sütun kimi
 * yerde sınıfsız. */
.anat-row {{
    display: grid;
    grid-template-columns: minmax(110px, 27%) 1fr;
    gap: 2px 18px;
    padding: 9px 0;
    border-top: 1px solid {p['border']};
    text-align: left;
}}
.anat-row:first-child {{ border-top: none; padding-top: 2px; }}
.anat-row:last-child {{ padding-bottom: 2px; }}
.anat-row > span {{
    font-size: 13.8px;
    line-height: 1.6;
    color: {p['text_muted']};
}}
.anat-row > span:first-child {{
    font-weight: 660;
    color: {p['text']};
}}
.anat-row code {{ font-size: 12.8px; }}

/* Akış: kutular ve aralarında oklar. */
.fig .flow {{
    display: flex;
    align-items: stretch;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
}}
.fig .flow .node {{
    flex: 0 1 auto;
    min-width: 96px;
    background: {p['surface_alt']};
    border: 1px solid {p['border']};
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 13.5px;
    line-height: 1.45;
    text-align: center;
    /* Kutu **blok** olmali, flex degil. Flex'ken icindeki `<br>` ayri bir
     * flex ogesine donusuyor ve satiri kirmiyordu: "Belirtime" ile
     * "hic bakmaz" ekranda bitisik yaziliyordu. `align-self` ile de dikey
     * ortalama korunuyor. */
    display: block;
    align-self: center;
}}
.fig .flow .node b {{ font-weight: 640; }}
.fig .flow .node code {{ font-size: 12.8px; }}
.fig .flow .node.ok {{
    background: {p['success_soft']};
    border-color: {p['success']};
    color: {p['success']};
}}
.fig .flow .node.no {{
    background: {p['danger_soft']};
    border-color: {p['danger']};
    color: {p['danger']};
}}
.fig .flow .node.acc {{
    background: {p['accent_soft']};
    border-color: {p['accent']};
    color: {p['accent']};
}}
.fig .flow .arrow {{
    display: flex;
    align-items: center;
    color: {p['text_muted']};
    font-size: 17px;
}}

/* Yan yana karşılaştırma: solda "böyle değil", sağda "böyle". */
.fig .versus {{ display: flex; gap: 14px; flex-wrap: wrap; }}
.fig .versus > div {{ flex: 1 1 210px; min-width: 0; }}
/* Başlık iki etiketle de yazılmış (`h4` 104, `h5` 36 yerde); ikisi de
 * aynı görünüyor. */
.fig .versus h4,
.fig .versus h5 {{
    font-size: 12.5px;
    font-weight: 660;
    letter-spacing: .02em;
    margin-bottom: 8px;
    text-align: left;
}}
.fig .versus .no h4,
.fig .versus .no h5 {{ color: {p['danger']}; }}
.fig .versus .ok h4,
.fig .versus .ok h5 {{ color: {p['success']}; }}
/* Yanlis degil, yalnizca daha az bilgi veren taraf. Kirmizi kullanilirsa
 * ogrenci onu hata sanip duzeltmeye calisiyor. */
.fig .versus .dim h4,
.fig .versus .dim h5 {{ color: {p['text_muted']}; }}
.fig .versus pre {{ margin: 0; }}

/* --- alıştırma yönergesi -------------------------------------------- */

.chips {{ display: flex; gap: 8px; margin: 10px 0 22px; flex-wrap: wrap; }}
.chip {{
    font-size: 12px; font-weight: 650; padding: 5px 11px;
    border-radius: 999px; background: {p['surface_alt']}; color: {p['text_muted']};
}}
.chip.easy {{ background: {p['success_soft']}; color: {p['success']}; }}
.chip.mid  {{ background: {p['warning_soft']}; color: {p['warning']}; }}
.chip.hard {{ background: {p['danger_soft']};  color: {p['danger']}; }}

.hintbox {{
    margin-top: 26px; border: 1px solid {p['border']};
    border-radius: 18px; overflow: hidden;
}}
.hintbox .hd {{
    padding: 14px 18px; background: {p['surface_alt']};
    font-size: 13.5px; font-weight: 650; color: {p['text']};
}}
.hint {{
    border-top: 1px solid {p['border']}; padding: 14px 18px;
    display: flex; gap: 13px; align-items: flex-start;
}}
.hint .lv {{
    flex: 0 0 26px; height: 26px; border-radius: 50%;
    background: {p['accent_soft']}; color: {p['accent']};
    display: grid; place-items: center; font-size: 12.5px; font-weight: 750;
}}
.hint .tx {{ flex: 1; font-size: 13.8px; color: {p['text_muted']}; }}
.hint .tx.open {{ color: {p['text']}; }}
.hint .tx.open p {{ margin: 0 0 8px; }}
.hint .tx.open pre {{ margin: 10px 0 0; }}
.hint a.show {{
    font-size: 12.5px; font-weight: 650; text-decoration: none;
    border: 1px solid {p['border_strong']}; background: {p['surface']};
    color: {p['text']}; border-radius: 8px; padding: 6px 13px; white-space: nowrap;
}}
.hint a.show:hover {{ background: {p['surface_hover']}; }}
.hint a.show.hide {{
    border-color: transparent; background: transparent; color: {p['text_muted']};
}}
.hint a.show.hide:hover {{ background: {p['surface_hover']}; color: {p['text']}; }}

/* --- sürüm notları -------------------------------------------------- */

.relcard {{
    display: block;
    background: {p['surface']}; border: 1px solid {p['border']};
    border-radius: 18px; padding: 0; margin-bottom: 16px; overflow: hidden;
    box-shadow: 0 6px 24px rgba(0, 0, 0, {'.35' if mode == 'dark' else '.07'});
}}
.relcard > .v {{ cursor: pointer; padding: 20px 24px; user-select: none; }}
.relcard > .v:hover {{ background: {p['surface_hover']}; }}
.relcard .kids {{ display: grid; grid-template-rows: 0fr; transition: grid-template-rows 420ms var(--spring); }}
.relcard.open .kids {{ grid-template-rows: 1fr; }}
.relcard .kids > div {{ overflow: hidden; }}
.relcard .inner {{ padding: 0 24px 22px; }}
.relcard .v {{ display: flex; align-items: center; gap: 12px; }}
.relcard .v b {{ font-family: {FONTS['display']}; font-size: 20px; font-weight: 700; color: {p['text']}; }}
.relcard .v .chev {{
    width: 18px; height: 18px; flex: none; color: {p['text_muted']};
    transition: transform 420ms var(--spring);
}}
.relcard.open .v .chev {{ transform: rotate(180deg); }}
.relcard .v .new {{
    background: {p['accent_soft']}; color: {p['accent']}; font-size: 11px; font-weight: 750;
    padding: 3px 9px; border-radius: 999px; letter-spacing: .4px;
}}
/* Yapım aşaması rozeti. "YENİ" gibi dolu değil, çerçeveli ve sakin —
   dikkat çekmesi değil, bilgi vermesi gerekiyor. */
.relcard .v .stage {{
    /* Yazı rengi zeminden geliyor: açık temada rozet koyu, koyu temada
       açık ton. Sabit beyaz yazsaydık koyu temada okunmazdı. */
    font-size: 11px; font-weight: 750; letter-spacing: .6px;
    padding: 3px 10px; border-radius: 999px;
}}
/* Alpha kırmızı, açık beta turuncu: ikisi aynı renkte olsaydı sürüm
   listesinde hangisinin ne olduğu ayırt edilmezdi. */
.relcard .v .stage.alpha {{ background: {p['danger_soft']}; color: {p['danger']}; }}
.relcard .v .stage.beta {{ background: {p['warning_soft']}; color: {p['warning']}; }}
.relcard .v .dt {{ color: {p['text_muted']}; font-size: 13px; margin-left: auto; }}
.relcard h4 {{
    font-size: 12px; font-weight: 800; color: {p['text_muted']};
    text-transform: uppercase; letter-spacing: 1.4px; margin: 10px 0 8px;
}}
.relcard ul {{ margin: 0; padding-left: 20px; }}
.relcard li {{ margin: 6px 0; font-size: 14.5px; color: {p['text']}; }}

/* --- bağlantı ve proje kartları ------------------------------------- */

/* Kartlar ikişerli dizilir; alt alta uzayan tek sütun hem yer israfı hem
 * dördünü bir arada görmeyi engelliyordu. Dar pencerede tek sütuna düşer. */
.cardgrid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 14px;
    align-items: stretch;
}}

.linkcard {{
    display: flex; flex-direction: column; text-decoration: none;
    background: {p['surface']}; border: 1px solid {p['border']};
    border-radius: 18px; padding: 20px 24px;
    box-shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
}}
.linkcard:hover {{ border-color: {p['accent']}; }}
.linkcard .row {{ display: flex; align-items: center; gap: 12px; }}
.linkcard b {{ font-size: 16.5px; font-weight: 660; color: {p['text']}; }}
.linkcard .go {{
    margin-left: auto; color: {p['accent']}; font-size: 14px; font-weight: 650;
    white-space: nowrap;
}}
.linkcard p {{ margin: 8px 0 0; font-size: 14px; color: {p['text_muted']}; flex: 1; }}
.linkcard .url {{
    margin-top: 12px; font-family: {FONTS['mono']}; font-size: 12px;
    color: {p['text_muted']}; word-break: break-all; opacity: .8;
}}

.who {{
    display: flex; align-items: center; gap: 18px; margin-bottom: 30px;
    padding: 24px 26px; border-radius: 24px;
    background: linear-gradient(135deg, {p['accent']} 0%, {p['accent_second']} 100%);
}}
.who .av {{
    flex: 0 0 auto; width: 58px; height: 58px; border-radius: 50%;
    background: rgba(255,255,255,.22); color: #fff;
    display: grid; place-items: center; font-size: 23px; font-weight: 750;
}}
.who b {{ display: block; font-size: 21px; font-weight: 720; color: #fff; }}
.who span {{ font-size: 14px; color: rgba(255,255,255,.92); }}

.licensebox {{
    background: {p['code_bg']}; border: 1px solid {p['border']};
    border-radius: 12px; padding: 20px 22px; margin: 18px 0;
    font-family: {FONTS['mono']}; font-size: 12.5px;
    line-height: 1.75; white-space: pre-wrap; color: {p['text_muted']};
}}

/* Sürüm notlarının alt sayfa düğmeleri. */
.pager {{
    display: flex; align-items: center; justify-content: center; gap: 8px;
    margin: 34px 0 8px; flex-wrap: wrap;
}}
.pager .pg {{
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 38px; height: 38px; padding: 0 12px;
    border: 1px solid {p['border']}; border-radius: 10px;
    background: {p['surface']}; color: {p['text_muted']};
    font-size: 14px; font-weight: 600; text-decoration: none;
    transition: border-color .15s, color .15s, background .15s;
}}
.pager a.pg:hover {{
    color: {p['text']}; border-color: {p['accent']};
}}
.pager .pg.on {{
    background: {p['accent']}; border-color: {p['accent']};
    color: #FFFFFF;
}}
.pager .pg.off {{ opacity: .38; }}

/* --- hareket (ui-taslak.md §2; theme/motion.py ile aynı değerler) ------ */
:root {{
    --spring: linear(0, 0.021, 0.075, 0.152, 0.242, 0.338, 0.435, 0.529, 0.616, 0.695, 0.766, 0.827, 0.878, 0.921, 0.955, 0.982, 1.003, 1.017, 1.028, 1.034, 1.037, 1.038, 1.038, 1.035, 1.033, 1.029, 1.025, 1.022, 1.018, 1.015, 1.012, 1.009, 1.007, 1.005, 1.003, 1.002, 1.001, 1, 0.999, 0.999, 1);
    --bounce: linear(0, 0.043, 0.154, 0.304, 0.472, 0.638, 0.79, 0.919, 1.019, 1.092, 1.137, 1.159, 1.162, 1.151, 1.13, 1.105, 1.077, 1.051, 1.027, 1.007, 0.992, 0.982, 0.976, 0.974, 0.974, 0.976, 0.98, 0.984, 0.989, 0.993, 0.997, 1, 1.002, 1.003, 1.004, 1.004, 1.004, 1.004, 1.003, 1.002, 1);
    --out: cubic-bezier(.33,1,.68,1);
}}
@keyframes sIn {{ from {{ opacity: 0; transform: translateY(8px); }} }}
@keyframes pgIn {{ from {{ opacity: 0; transform: translateY(16px); }} }}
.pgin {{ animation: pgIn 180ms var(--out); }}
/* Hakkında: bütün bölümler sayfada, görünen `.on`; sekme değişince `.anim`. */
.absec {{ display: none; }}
.absec.on {{ display: block; }}
.absec.anim {{ animation: pgIn 180ms var(--out); }}
@keyframes pop {{ from {{ transform: scale(0); opacity: 0; }} }}
@keyframes grow {{ from {{ width: 0; }} }}
@keyframes glowOnce {{ 40% {{ box-shadow: 0 0 0 6px {p['accent_soft']}; }} }}
/* Sıralı giriş: `.enter` kabının içindeki `.stg` öğeleri 40 ms arayla,
 * en fazla 8 öğe gecikir (B8). */
/* Bölüm ilerlemesi çubuğu değişince dolarak ilerliyor (C4). */
.prog .bar i {{ transition: width 700ms var(--out); }}
.enter .stg {{ animation: sIn 420ms var(--spring) both; animation-delay: calc(min(var(--n, 0), 7) * 40ms); }}

/* --- sürüm notları, Hakkında (C15) ---------------------------------------- */
.enter .relcard, .enter .linkcard, .enter .faq {{ animation: sIn 420ms var(--spring) both; }}
.enter .relcard:nth-child(2), .enter .linkcard:nth-child(2), .enter .faq:nth-of-type(2) {{ animation-delay: 40ms; }}
.enter .relcard:nth-child(3), .enter .linkcard:nth-child(3), .enter .faq:nth-of-type(3) {{ animation-delay: 80ms; }}
.enter .relcard:nth-child(4), .enter .linkcard:nth-child(4), .enter .faq:nth-of-type(4) {{ animation-delay: 120ms; }}
.enter .relcard:nth-child(n+5), .enter .linkcard:nth-child(n+5), .enter .faq:nth-of-type(n+5) {{ animation-delay: 160ms; }}
.linkcard {{ transition: transform 240ms var(--out), box-shadow 240ms var(--out), border-color 120ms var(--out); }}
.linkcard:hover {{ transform: translateY(-2px); box-shadow: 0 14px 36px rgba(0,0,0,.28);
    transition: transform 420ms var(--spring), box-shadow 240ms var(--out); }}
.linkcard .go {{ transition: transform 420ms var(--spring); display: inline-block; }}
.linkcard:hover .go {{ transform: translateX(3px); }}
.faq > .q .mark::after {{ transition: transform 420ms var(--spring), opacity 180ms; }}
.faq.open > .q .mark::after {{ transform: rotate(90deg); }}

/* --- rotalar --------------------------------------------------------- */

/* Adımlar solda numaralı bir zaman çizgisine diziliyor; numaraları
 * birleştiren çizgi `li::before`. Son adımda çizgi yok. */
/* `.content ol` ve `.content li` kendi boşluklarını veriyor; seçici onları
 * geçecek kadar özgül olmalı, yoksa liste sola kayıyor. */
.content .route {{ list-style: none; margin: 30px 0 0; padding: 0; }}
.content .rstep {{ position: relative; display: flex; gap: 18px; margin: 0; padding-bottom: 16px; }}
.rstep::before {{
    content: ""; position: absolute; left: 22px; top: 46px; bottom: 0;
    width: 2px; background: {p['border']};
}}
.rstep:last-child::before {{ display: none; }}
.rstep.done::before {{ background: {p['success']}; opacity: .45; }}

.rnum {{
    flex: 0 0 46px; height: 46px; border-radius: 50%; box-sizing: border-box;
    display: grid; place-items: center; position: relative; z-index: 1;
    background: {p['surface']}; border: 2px solid {p['border_strong']};
    color: {p['text_muted']}; font-family: {FONTS['display']}; font-size: 16px; font-weight: 700;
}}
.rstep.next .rnum {{ background: {p['accent']}; border-color: {p['accent']}; color: #fff;
    box-shadow: 0 0 0 5px {p['accent_soft']}; }}
.rstep.done .rnum {{ background: {p['success_soft']}; border-color: {p['success']}; color: {p['success']}; }}

.rcard {{
    flex: 1; min-width: 0; display: flex; gap: 16px; align-items: flex-start;
    background: {p['surface']}; border: 1px solid {p['border']};
    border-radius: 16px; padding: 18px 20px 18px;
    transition: transform 240ms var(--out), box-shadow 240ms var(--out), border-color 120ms var(--out);
}}
.rcard:hover {{ transform: translateY(-2px); box-shadow: 0 14px 36px rgba(0,0,0,.28);
    transition: transform 420ms var(--spring), box-shadow 240ms var(--out); }}
.rbody {{ flex: 1; min-width: 0; }}
.rlogo {{ flex: none; width: 44px; height: 44px; transition: transform 420ms var(--spring); }}
.rlogo svg {{ width: 44px; height: 44px; display: block; }}
.rcard:hover .rlogo {{ transform: rotate(-6deg) scale(1.08); }}
.rstep.next .rcard {{ border-color: {p['accent']}; box-shadow: 0 0 0 3px {p['accent_soft']}; }}
.enter .rstep.next .rcard {{ animation: glowOnce 1400ms var(--out) 400ms; }}
.enter .rfoot .bar i {{ animation: grow 700ms var(--out) both; animation-delay: 250ms; }}
.rstep.soon .rcard {{ background: transparent; border-style: dashed; }}
.rstep.soon .rhead b, .rstep.soon .ricon {{ opacity: .7; }}

.rhead {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.rhead b {{ font-family: {FONTS['display']}; font-size: 17px; font-weight: 700; color: {p['text']}; margin-right: 2px; }}
.rtag {{
    font-size: 11.5px; font-weight: 680; padding: 3px 9px; border-radius: 999px;
    background: {p['surface_alt']}; color: {p['text_muted']}; white-space: nowrap;
}}
.rtag.next {{ background: {p['accent_soft']}; color: {p['accent']}; }}
.rtag.ok {{ background: {p['success_soft']}; color: {p['success']}; }}
.rtag.soon {{ background: {p['warning_soft']}; color: {p['warning']}; }}

.rcard p {{ margin: 4px 0 0; font-size: 14px; line-height: 1.65; color: {p['text_muted']}; }}
/* Rota girişi (prototip `.route .intro`). */
.content p.route-intro {{ color: {p['text_muted']}; font-size: 15.5px; line-height: 1.7; }}
.content h1.route-title {{ font-size: 32px; margin: 6px 0 10px; }}

/* Adımın açıklaması: "Bu adımda" maddeleri, "Sonunda" kutusu, odak
 * bölümlerinin listesi (Alican 29 Eylül: rotalar daha açıklayıcı olsun). */
.rlabel {{
    display: block; font-size: 11.5px; font-weight: 700; letter-spacing: .06em;
    text-transform: uppercase; color: {p['text_muted']}; margin-bottom: 6px; opacity: .8;
}}
.rlearn {{ margin-top: 14px; }}
.content .rlearn ul {{
    list-style: none; margin: 0; padding: 0;
    display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 4px 18px;
}}
.content .rlearn li {{
    position: relative; margin: 0; padding-left: 16px;
    font-size: 13.5px; line-height: 1.5; color: {p['text']};
}}
.rlearn li::before {{
    content: ""; position: absolute; left: 2px; top: .6em; width: 6px; height: 6px;
    border-radius: 50%; background: {p['accent']}; opacity: .8;
}}
.rgain {{
    margin-top: 12px; padding: 9px 12px; border-radius: 10px;
    background: {p['accent_soft']}; font-size: 13.5px; line-height: 1.55; color: {p['text']};
}}
.rgain b {{ color: {p['accent']}; font-weight: 700; }}
.rstep.soon .rgain {{ background: {p['surface_alt']}; }}
.rstep.soon .rgain b {{ color: {p['text_muted']}; }}

.rfocus {{ margin-top: 14px; display: flex; flex-direction: column; gap: 6px; }}
.rsec {{
    display: flex; gap: 10px; align-items: flex-start; padding: 8px 10px;
    border: 1px solid {p['border']}; border-radius: 10px; text-decoration: none;
    transition: border-color 120ms var(--out), background 120ms var(--out);
}}
a.rsec:hover {{ border-color: {p['accent']}; background: {p['accent_soft']}; }}
.rsec > i {{
    flex: none; width: 18px; height: 18px; margin-top: 1px; border-radius: 50%;
    border: 2px solid {p['border_strong']}; box-sizing: border-box;
    display: grid; place-items: center; font-style: normal; font-size: 11px; font-weight: 800;
}}
.rsec.done > i {{ border-color: {p['success']}; background: {p['success']}; color: #fff; }}
.rsec > span {{ display: flex; flex-direction: column; gap: 1px; min-width: 0; }}
.rsec b {{ font-size: 13.5px; font-weight: 650; color: {p['text']}; }}
.rsec small {{ font-size: 12.5px; line-height: 1.45; color: {p['text_muted']}; }}
.rsec.locked {{ opacity: .6; }}

.rfoot {{ display: flex; align-items: center; gap: 14px; margin-top: 14px; }}
.rfoot .bar {{ flex: 1; margin: 0; }}
.rcount {{ font-size: 12.5px; color: {p['text_muted']}; white-space: nowrap; }}
.rgo {{
    font-size: 13.5px; font-weight: 650; color: {p['accent']};
    text-decoration: none; white-space: nowrap;
}}
.rgo:hover {{ text-decoration: underline; }}

/* --- sık sorulanlar -------------------------------------------------- */

/* Akordeon: başlığa basınca sayfa içinde `.open` değişiyor, cevap
 * yüksekliği yayla açılıyor (prototip `.faq .kids`). Uygulamaya haber
 * gerekmiyor; iş sayfanın içinde bitiyor. */
.faqlist {{ display: flex; flex-direction: column; gap: 10px; margin-top: 26px; }}

.faq {{
    border: 1px solid {p['border']};
    border-radius: 14px;
    background: {p['surface_alt']};
    overflow: hidden;
}}
.faq.open {{ border-color: {p['border_strong']}; }}

/* Soru: koyu zeminli başlık. Cevabın zeminiyle arasındaki fark, hangisinin
 * soru hangisinin cevap olduğunu okumadan belli ediyor. */
.faq > .q {{
    cursor: pointer; user-select: none;
    padding: 16px 52px 16px 20px;
    position: relative;
    background: {p['surface_alt']};
    font-weight: 650;
    font-size: 15px;
    color: {p['text']};
}}
.faq > .q:hover {{ color: {p['accent']}; }}

/* Sağdaki artı işareti açıkken eksiye dönüyor. İki ayrı çizgi olarak
 * çiziliyor; dikey olan açılınca kayboluyor. */
.faq > .q .mark {{
    position: absolute; right: 20px; top: 50%;
    width: 13px; height: 13px; margin-top: -7px;
}}
.faq > .q .mark::before,
.faq > .q .mark::after {{
    content: ""; position: absolute; background: {p['text_muted']};
    border-radius: 1px;
}}
.faq > .q .mark::before {{ left: 0; top: 6px; width: 13px; height: 2px; }}
.faq > .q .mark::after {{ left: 6px; top: 0; width: 2px; height: 13px; }}
.faq.open > .q .mark::after {{ opacity: 0; }}
.faq.open > .q {{ color: {p['accent']}; }}

.faq .kids {{ display: grid; grid-template-rows: 0fr; transition: grid-template-rows 420ms var(--spring); }}
.faq.open .kids {{ grid-template-rows: 1fr; }}
.faq .kids > div {{ overflow: hidden; }}
.faq .answer {{
    padding: 4px 20px 6px;
    background: {p['bg']};
    border-top: 1px solid {p['border']};
}}
.faq .answer p {{ margin: 12px 0; font-size: 14.5px; color: {p['text_muted']}; }}
.faq .answer code {{ font-size: 13px; }}


/* --- alt gezinme ---------------------------------------------------- */

.foot {{
    display: flex; gap: 12px; margin-top: 48px;
    padding-top: 28px; border-top: 1px solid {p['border']};
}}
.foot a {{
    font-size: 14.5px; font-weight: 600; border-radius: 11px;
    padding: 12px 22px; cursor: pointer; text-decoration: none;
    border: 1px solid {p['border_strong']};
    background: {p['surface']}; color: {p['text']};
}}
.foot a:hover {{ background: {p['surface_hover']}; }}
.foot a.pri {{
    background: {p['accent']}; border-color: {p['accent']}; color: #fff;
}}
.foot a.pri:hover {{ background: {p['accent_hover']}; }}
.foot a.sp {{ margin-left: auto; }}
.foot a.off {{ opacity: .4; pointer-events: none; }}
"""
