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

aside.toc {{ grid-column: 3; padding-left: 36px; }}

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
.toc-inner a.on {{
    color: {p['accent']}; border-left-color: {p['accent']}; font-weight: 600;
}}
.toc-inner a:hover {{ color: {p['text']}; }}

.prog {{
    margin-top: 24px; padding: 16px;
    background: {p['surface_alt']}; border-radius: 12px;
}}
.prog .h2 {{ font-size: 12.5px; color: {p['text_muted']}; margin-bottom: 9px; }}
.bar {{ height: 7px; background: {p['border']}; border-radius: 4px; overflow: hidden; }}
.bar i {{ display: block; height: 100%; background: {p['accent']}; border-radius: 4px; }}

/* --- metin ---------------------------------------------------------- */

.content h1 {{
    font-size: 31px; font-weight: 720; letter-spacing: -.6px;
    margin-bottom: 10px; color: {p['text']};
}}
.content h2 {{
    font-size: 20px; font-weight: 670; margin: 36px 0 12px;
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
figure.fig svg .ink {{ fill: {p['text']}; }}
figure.fig svg .dim {{ fill: {p['text_muted']}; }}
figure.fig svg .box {{ fill: {p['surface_alt']}; stroke: {p['border_strong']}; }}
figure.fig svg .line {{ fill: none; stroke: {p['border_strong']}; stroke-width: 1.5; }}

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
.fig .versus h5 {{
    font-size: 12.5px;
    font-weight: 660;
    letter-spacing: .02em;
    margin-bottom: 8px;
    text-align: left;
}}
.fig .versus .no h5 {{ color: {p['danger']}; }}
.fig .versus .ok h5 {{ color: {p['success']}; }}
/* Yanlis degil, yalnizca daha az bilgi veren taraf. Kirmizi kullanilirsa
 * ogrenci onu hata sanip duzeltmeye calisiyor. */
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

/* --- sürüm notları -------------------------------------------------- */

.relcard {{
    background: {p['surface']}; border: 1px solid {p['border']};
    border-radius: 18px; padding: 26px 30px; margin-bottom: 20px;
    box-shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
}}
.relcard .v {{ display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }}
.relcard .v b {{ font-size: 19px; font-weight: 700; color: {p['text']}; }}
.relcard .v .new {{
    background: {p['accent']}; color: #fff; font-size: 11px; font-weight: 750;
    padding: 3px 9px; border-radius: 999px; letter-spacing: .4px;
}}
/* Yapım aşaması rozeti. "YENİ" gibi dolu değil, çerçeveli ve sakin —
   dikkat çekmesi değil, bilgi vermesi gerekiyor. */
.relcard .v .stage {{
    /* Yazı rengi zeminden geliyor: açık temada rozet koyu, koyu temada
       açık ton. Sabit beyaz yazsaydık koyu temada okunmazdı. */
    color: {p['bg']};
    font-size: 11px; font-weight: 750; letter-spacing: .6px;
    padding: 3px 10px; border-radius: 8px;
}}
/* Alpha kırmızı, açık beta turuncu: ikisi aynı renkte olsaydı sürüm
   listesinde hangisinin ne olduğu ayırt edilmezdi. */
.relcard .v .stage.alpha {{ background: {p['danger']}; }}
.relcard .v .stage.beta {{ background: {p['warning']}; }}
.relcard .v .dt {{ color: {p['text_muted']}; font-size: 13px; margin-left: auto; }}
.relcard h4 {{
    font-size: 13px; font-weight: 700; color: {p['text_muted']};
    text-transform: uppercase; letter-spacing: .6px; margin: 18px 0 8px;
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

/* --- sık sorulanlar -------------------------------------------------- */

/* Akordeon `<details>`/`<summary>` ile: açılıp kapanmayı tarayıcı kendi
 * yapıyor, betiğe gerek kalmıyor. Sayfa uygulamaya kendiliğinden haber
 * veremediği için betikle çözülen bir akordeon burada zaten çalışmazdı. */
.faqlist {{ display: flex; flex-direction: column; gap: 10px; margin-top: 26px; }}

.faq {{
    border: 1px solid {p['border']};
    border-radius: 14px;
    background: {p['surface_alt']};
    overflow: hidden;
}}
.faq[open] {{ border-color: {p['border_strong']}; }}

/* Soru: koyu zeminli başlık. Cevabın zeminiyle arasındaki fark, hangisinin
 * soru hangisinin cevap olduğunu okumadan belli ediyor. */
.faq > summary {{
    list-style: none;
    cursor: pointer;
    padding: 16px 52px 16px 20px;
    position: relative;
    background: {p['surface_alt']};
    font-weight: 650;
    font-size: 15px;
    color: {p['text']};
}}
.faq > summary::-webkit-details-marker {{ display: none; }}
.faq > summary:hover {{ color: {p['accent']}; }}

/* Sağdaki artı işareti açıkken eksiye dönüyor. İki ayrı çizgi olarak
 * çiziliyor; dikey olan açılınca kayboluyor. */
.faq > summary .mark {{
    position: absolute; right: 20px; top: 50%;
    width: 13px; height: 13px; margin-top: -7px;
}}
.faq > summary .mark::before,
.faq > summary .mark::after {{
    content: ""; position: absolute; background: {p['text_muted']};
    border-radius: 1px;
}}
.faq > summary .mark::before {{ left: 0; top: 6px; width: 13px; height: 2px; }}
.faq > summary .mark::after {{ left: 6px; top: 0; width: 2px; height: 13px; }}
.faq[open] > summary .mark::after {{ opacity: 0; }}
.faq[open] > summary {{ color: {p['accent']}; }}

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
