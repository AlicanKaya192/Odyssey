"""Belge alanlarının stili.

Konu anlatımı, ders notları ve alıştırma yönergesi `QWebEngineView` ile
çiziliyor. O motor Chromium olduğu için maketteki CSS burada birebir
çalışıyor — Qt'nin kendi metin motorunda desteklenmeyen yuvarlak köşe,
gölge, kod renklendirmesi ve yazı tipi ağırlıkları dahil.

Kurallar `Plan/tasarim/maket.html` dosyasındaki `.content` bloğuyla aynı
tutuluyor. Renkler ve ölçüler `tokens.py`'den geliyor, elle yazılmıyor.
"""

from __future__ import annotations

from .tokens import FONTS, PALETTES, READING_WIDTH, TOC_WIDTH


def build_css(mode: str) -> str:
    """Belge stilini seçili temaya göre üretir."""
    p = PALETTES.get(mode, PALETTES["light"])

    return f"""
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

.footnote {{
    margin-top: 40px; padding-top: 22px;
    border-top: 1px solid {p['border']};
    font-size: 13px; color: {p['text_muted']}; text-align: center;
}}

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
