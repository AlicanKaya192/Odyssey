"""Bölümün videosu: YouTube'daki ders kaydı, programın içinde.

CS50 Python patikasında her haftanın dersi bir YouTube videosu; CS50'nin
kendi sitesindeki gibi sekme açılınca oynatıcı yükleniyor (Alican 22 Ekim:
"direk video düşsün, sitedeki gibi"). Bu, programın Google'a bağlandığı tek
yer; `CODE_SIGNING.md`'nin gizlilik bölümünde yazılı.

Üç şey ölçülerek seçildi (22 Ekim): gömme adresini doğrudan açmak "oynatıcı
yapılandırma hatası" veriyor, yerel (`file:`) sayfadaki iframe hiç açılmıyor;
oynatıcı yalnızca **https taban adresli** bir sayfanın içindeki iframe'de
çalışıyor (YouTube gömen sayfanın adresini istiyor). Sayfa `setHtml` ile
veriliyor, `BASE_URL` hiçbir yere istek atmıyor.

**Kontrol çubuğu bizim** (YouTube'unki `controls=0` ile kapalı): Alican'ın
ekranında YouTube'un çubuğu kaybolmuyor ve altyazının üstüne biniyordu.
Çubuk videonun altında, video alanında altyazıdan başka bir şey yok.
Çubuk sağ uçtaki düğmeyle gizlenebiliyor; gizliyken videonun altında küçük
bir tutamak kalıyor (Alican 23 Ekim), tercih `video_bar`. Altyazı `C` ile
açılıp kapanıyor; kısayol Qt düzeyinde de var, çünkü videoya tıklanınca
tuşlar YouTube'un çerçevesine gidiyor.
YouTube'un IFrame API'si (oynat, sar, hız, altyazı) sayfanın içinden;
**kalite** API'de yok (`setPlaybackQuality` etkisiz), oynatıcının kendi
nesnesine Qt'nin çerçeve erişimiyle veriliyor (`_apply_quality`; ölçüldü:
720p seçen oynatıcı 1080p'ye geçti). Sayfa uygulamaya **başlığıyla**
haber veriyor (`document.title = "q:hd720#3"`): kanal kurmaya değmeyecek
kadar az şey (kalite, altyazı, boyut, "oynamaya başladı"). Tercihler
ayarlarda saklanıyor (`video_quality`, `video_caption_lang`,
`video_caption_size`).

**Altyazı da bizim** (Alican 23 Ekim: "Türkçe altyazı da olsun"): YouTube'un
altyazısı hiç açılmıyor; bölümdeki SRT dosyaları (CS50'nin İngilizcesi,
bizim Türkçe çevirimiz, `core/subtitles.py`) sayfaya veriliyor ve oynatıcının
saniyesine göre videonun üstüne yazılıyor. İki dil aynı görünüşte, A−/A+
ikisine de uyuyor, tam ekranda da duruyor. Varsayılan dil arayüzün dili.

- Profil **gizli** (`profile()`): çerez ve önbellek diske yazılmıyor.
- Ana çerçeve dış siteye gitmiyor, yeni pencere açılmıyor: video yalnızca
  programda (Alican: "ek site atma yok").
- İnternet yoksa uyarı; bağlantı gelince video kendiliğinden yükleniyor.
- Başka sekmeye geçince duraklıyor, bölümden çıkınca sayfa boşaltılıyor
  (arkada ses kalmasın).
"""

from __future__ import annotations

import html
import json
from typing import Callable

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import subtitles
from ..core.language import LanguageManager
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING

BASE_URL = "https://odyssey.local/"
EMBED_URL = ("https://www.youtube.com/embed/{id}?enablejsapi=1&controls=0&rel=0&iv_load_policy=3"
             "&playsinline=1&hl={lang}&origin=https%3A%2F%2Fodyssey.local")
QUALITIES = ("auto", "hd1080", "hd720", "large")
# `lang` boşsa (hiç seçilmemiş) altyazı arayüzün dilinde açılıyor, o dil yoksa ilk olanda.
# `bar`: kontrol çubuğu görünür mü (Alican 23 Ekim: gizlenip istenince açılsın).
DEFAULT_PREFS = {"lang": "", "size": 0, "quality": "hd1080", "bar": True}
# Kendi altyazımızın dilleri ve menüdeki adları (dilin kendi adıyla).
SUBTITLE_LANGS = {"en": "English", "tr": "Türkçe"}
# Oynatıcının kendi nesnesi; `setPlaybackQualityRange` IFrame API'sinde yok.
QUALITY_JS = ("(() => {{ const p = document.querySelector('#movie_player');"
              " if (p && p.setPlaybackQualityRange) p.setPlaybackQualityRange('{q}', '{q}'); }})()")

_PROFILE: QWebEngineProfile | None = None


def profile() -> QWebEngineProfile:
    """Videoların ortak gizli profili; uygulama kapanana kadar yaşıyor.

    Sayfalardan önce silinmesin diye uygulamaya bağlı (profil sayfadan önce
    giderse Qt uyarı veriyor).
    """
    global _PROFILE
    if _PROFILE is None:
        _PROFILE = QWebEngineProfile(QApplication.instance())
    return _PROFILE


_ICONS = {
    "play": '<path d="M8 5.6v12.8a1 1 0 0 0 1.5.9l10-6.4a1 1 0 0 0 0-1.8l-10-6.4A1 1 0 0 0 8 5.6z" fill="currentColor"/>',
    "pause": '<rect x="6.5" y="5" width="4" height="14" rx="1.2" fill="currentColor"/>'
             '<rect x="13.5" y="5" width="4" height="14" rx="1.2" fill="currentColor"/>',
    "back": '<path d="M11 7 6 12l5 5M18 7l-5 5 5 5" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
    "fwd": '<path d="m13 7 5 5-5 5M6 7l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"/>',
    "fs": '<path d="M4 9V5h4M20 9V5h-4M4 15v4h4M20 15v4h-4" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "chevron": '<path d="m7 14 5-5 5 5" fill="none" stroke="currentColor" stroke-width="2.2" '
               'stroke-linecap="round" stroke-linejoin="round"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" '
             'stroke-linecap="round" stroke-linejoin="round"/>',
    "down": '<path d="m7 10 5 5 5-5" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
}


def _svg(name: str, size: int = 20) -> str:
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}">{_ICONS[name]}</svg>'


def _picker(key: str, title: str, options: list[tuple], head: str = "") -> str:
    """Kendi açılır seçicimiz (altyazı, hız, kalite): düğme ve üstüne açılan liste.

    `<select>` kullanılmıyor: açılan listesi Chromium'un yerel menüsü,
    CSS'le boyanamıyor; temadan kopuk, mavi vurgulu bir Windows listesi
    çıkıyordu (Alican bildirdi). Seçenek `(değer, etiket)` ya da düğmede
    kısa yazı gösterilecekse `(değer, etiket, kısa)`.
    """
    satirlar = "".join(
        f'<div class="opt" role="option" tabindex="-1" data-value="{html.escape(o[0], quote=True)}"'
        + (f' data-short="{html.escape(o[2], quote=True)}"' if len(o) > 2 else "")
        + f'><span>{html.escape(o[1])}</span>{_svg("check", 16)}</div>' for o in options)
    return (f'<div class="picker"><button class="pick" id="{key}" title="{title}" aria-haspopup="listbox" '
            f'aria-expanded="false"><span class="val"></span>{_svg("chevron", 14)}</button>'
            f'<div class="menu" id="{key}-menu" role="listbox" hidden><div class="head">{head or title}</div>'
            f'{satirlar}</div></div>')


def embed_html(video_id: str, language: LanguageManager, palette: dict, prefs: dict,
               subs: dict[str, list] | None = None) -> str:
    """Oynatıcı (16:9, ortada), üstünde kendi altyazımız, altında kendi kontrol çubuğumuz.

    subs: {dil: [(başlangıç, bitiş, yazı), ...]}; `prefs["lang"]` bunlardan
    biri ya da "off"."""
    t = language.t
    subs = subs or {}
    kaynak = html.escape(EMBED_URL.format(id=video_id, lang=language.language), quote=True)
    etiket = {k: t(f"video.{k}") for k in ("play", "pause", "back10", "fwd10", "captions", "smaller",
                                           "larger", "speed", "quality", "auto", "fullscreen",
                                           "subtitles", "subtitles_off", "hide_bar", "show_bar")}
    renk = {k: html.escape(palette[k], quote=True)
            for k in ("bg", "surface", "surface_hover", "border", "text", "text_muted", "accent")}
    a = lambda k: html.escape(etiket[k], quote=True)  # noqa: E731
    kalite_adi = {"auto": etiket["auto"], "hd1080": "1080p", "hd720": "720p", "large": "480p"}
    kalite = _picker("quality", a("quality"), [(q, kalite_adi[q]) for q in QUALITIES])
    hiz = _picker("speed", a("speed"), [(h, f"{h}×") for h in ("0.75", "1", "1.25", "1.5", "1.75", "2")])
    diller = [d for d in SUBTITLE_LANGS if subs.get(d)]
    altyazi = _picker("cc", a("captions"), [("off", etiket["subtitles_off"], "CC")]
                      + [(d, SUBTITLE_LANGS[d], f"CC · {d.upper()}") for d in diller],
                      head=a("subtitles"))
    tercih = language.language if language.language in diller else (diller or ["off"])[0]
    secili = prefs["lang"] if prefs["lang"] in diller or prefs["lang"] == "off" else tercih
    ayar = json.dumps({"prefs": {"lang": secili, "size": int(prefs["size"]), "quality": prefs["quality"],
                                 "bar": bool(prefs.get("bar", True))},
                       "subs": {d: [[round(s, 3), round(e, 3), y] for s, e, y in subs[d]] for d in diller},
                       "preferred": tercih,
                       "labels": {"play": etiket["play"], "pause": etiket["pause"]},
                       "icons": {"play": _svg("play"), "pause": _svg("pause")}}, ensure_ascii=False)
    ayar = ayar.replace("</", "<\\/")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
:root {{ --bg: {renk['bg']}; --surface: {renk['surface']}; --hover: {renk['surface_hover']};
  --border: {renk['border']}; --text: {renk['text']}; --muted: {renk['text_muted']}; --accent: {renk['accent']}; }}
html, body {{ margin: 0; height: 100%; background: var(--bg); color: var(--text); overflow: hidden;
  font: 13px "Segoe UI", system-ui, sans-serif; }}
body {{ display: flex; flex-direction: column; --chrome: 64px; }}
body.nobar {{ --chrome: 30px; }}
.stage {{ flex: 1; min-height: 0; display: grid; place-items: center; }}
.wrap {{ width: min(100%, calc((100vh - var(--chrome)) * 16 / 9)); aspect-ratio: 16 / 9; position: relative; }}
.subs {{ position: absolute; left: 50%; bottom: 7%; transform: translateX(-50%); width: 88%; text-align: center;
  pointer-events: none; --k: 1; }}
.subs span {{ display: inline; white-space: pre-line; color: #fff; background: rgba(8, 8, 12, .78);
  padding: .12em .5em; border-radius: 6px; line-height: 1.5; -webkit-box-decoration-break: clone;
  box-decoration-break: clone; font: 500 calc(clamp(14px, 1.75vw, 42px) * var(--k)) "Segoe UI", system-ui, sans-serif; }}
.subs span:empty {{ display: none; }}
iframe {{ width: 100%; height: 100%; border: 0; border-radius: 12px 12px 0 0; display: block; background: #000; }}
.bar {{ flex: none; display: flex; align-items: center; gap: 6px; padding: 8px 10px; margin: 0 auto 4px;
  width: min(100%, calc((100vh - var(--chrome)) * 16 / 9)); box-sizing: border-box; background: var(--surface);
  border: 1px solid var(--border); border-top: 0; border-radius: 0 0 12px 12px; }}
body.nobar .bar {{ display: none; }}
body.nobar iframe {{ border-radius: 12px; }}
/* Çubuğu gizleme düğmesi ve gizliyken kalan tutamak: göze batmayan ama görülen. */
#hidebar {{ color: var(--muted); min-width: 26px; padding: 0 3px; }}
#hidebar:hover, #showbar:hover {{ color: var(--text); }}
#showbar {{ display: none; flex: none; margin: 4px auto 6px; height: 18px; min-width: 0; width: 46px; padding: 0;
  color: var(--muted); background: var(--surface); border: 1px solid var(--border); border-radius: 9px;
  opacity: .75; }}
#showbar:hover {{ opacity: 1; background: var(--hover); }}
body.nobar #showbar {{ display: inline-grid; }}
button {{ font: inherit; color: var(--text); background: transparent; border: 0; border-radius: 8px;
  height: 32px; min-width: 32px; padding: 0 8px; cursor: pointer; display: inline-grid; place-items: center; }}
button:hover {{ background: var(--hover); }}
button:focus {{ outline: none; }}
button:focus-visible, .opt:focus-visible {{ outline: 2px solid var(--accent); outline-offset: -2px; }}
.picker {{ position: relative; }}
.pick {{ display: inline-flex; align-items: center; gap: 4px; padding: 0 8px 0 10px; font-variant-numeric: tabular-nums; }}
.pick svg {{ color: var(--muted); transition: transform .15s ease; }}
.pick[aria-expanded="true"] {{ background: var(--hover); }}
.pick[aria-expanded="true"] svg {{ transform: rotate(180deg); }}
.menu {{ position: absolute; right: 0; bottom: calc(100% + 10px); z-index: 10; min-width: 132px; padding: 6px;
  box-sizing: border-box; background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, .35); animation: rise .12s ease-out; }}
.menu[hidden] {{ display: none; }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
.head {{ padding: 6px 10px 6px; font-size: 11px; font-weight: 600; letter-spacing: .4px; color: var(--muted);
  white-space: nowrap; }}
.opt {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; height: 32px; padding: 0 10px;
  border-radius: 8px; cursor: pointer; white-space: nowrap; font-variant-numeric: tabular-nums; }}
.opt:hover, .opt:focus {{ background: var(--hover); outline: none; }}
.opt svg {{ visibility: hidden; color: var(--accent); }}
.opt[aria-selected="true"] {{ color: var(--accent); font-weight: 600; }}
.opt[aria-selected="true"] svg {{ visibility: visible; }}
#cc .val {{ font-weight: 700; letter-spacing: .5px; color: var(--muted); }}
#cc.on .val {{ color: var(--accent); }}
.nosubs #cc, .nosubs #smaller, .nosubs #larger {{ display: none; }}
#time {{ color: var(--muted); font-variant-numeric: tabular-nums; white-space: nowrap; padding: 0 4px; }}
#seek {{ flex: 1; min-width: 60px; accent-color: var(--accent); cursor: pointer; }}
.sep {{ width: 1px; height: 20px; background: var(--border); margin: 0 2px; }}
</style></head><body>
<div class="stage"><div class="wrap"><iframe id="yt" src="{kaynak}"
 allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
 referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<div class="subs" id="subs"><span id="subtext"></span></div></div></div>
<div class="bar{'' if diller else ' nosubs'}">
 <button id="play" title="{a('play')}">{_svg('play')}</button>
 <button id="back" title="{a('back10')}">{_svg('back')}</button>
 <button id="fwd" title="{a('fwd10')}">{_svg('fwd')}</button>
 <span id="time">0:00 / 0:00</span>
 <input id="seek" type="range" min="0" max="1000" value="0">
 <span class="sep"></span>
 {altyazi}
 <button id="smaller" title="{a('smaller')}">A−</button>
 <button id="larger" title="{a('larger')}">A+</button>
 {hiz}
 {kalite}
 <button id="fs" title="{a('fullscreen')}">{_svg('fs')}</button>
 <button id="hidebar" title="{a('hide_bar')}">{_svg('down', 18)}</button>
</div>
<button id="showbar" title="{a('show_bar')}">{_svg('chevron', 16)}</button>
<script>
const CFG = {ayar};
const S = CFG.prefs;
const $ = id => document.getElementById(id);
let player = null, dragging = false, n = 0;
function tell(m) {{ document.title = m + '#' + (++n); }}
function fmt(s) {{
  s = Math.max(0, Math.floor(s || 0));
  const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = String(s % 60).padStart(2, '0');
  return h ? h + ':' + String(m).padStart(2, '0') + ':' + x : m + ':' + x;
}}
// YouTube'un kendi altyazısı hiç açılmıyor: altyazıyı biz yazıyoruz (iki dil, aynı görünüş).
function youtubeCaptionsOff() {{ if (player && player.unloadModule) player.unloadModule('captions'); }}
const SIZES = [0.8, 1, 1.2, 1.45, 1.75];   // A− / A+: S.size -1..3
let shown = null;
function subAt(cues, t) {{
  let lo = 0, hi = cues.length - 1;
  while (lo <= hi) {{
    const mid = (lo + hi) >> 1;
    if (cues[mid][1] <= t) lo = mid + 1;
    else if (cues[mid][0] > t) hi = mid - 1;
    else return cues[mid];
  }}
  return null;
}}
function subTick() {{
  const cues = CFG.subs[S.lang];
  const cue = cues && player && player.getCurrentTime ? subAt(cues, player.getCurrentTime() || 0) : null;
  if (cue !== shown) {{ shown = cue; $('subtext').textContent = cue ? cue[2] : ''; }}
}}
function captions() {{
  $('subs').style.setProperty('--k', SIZES[S.size + 1]);
  $('cc').classList.toggle('on', S.lang !== 'off');
  shown = undefined;
  subTick();
}}
function setLang(v) {{
  S.lang = v;
  pickers.cc.set(v);
  if (v !== 'off') CFG.preferred = v;
  captions();
  tell('cl:' + v);
}}
// `c` ve uygulamanın C kısayolu: kapalıysa en son seçilen dile açar.
function toggleCaptions() {{ if (CFG.preferred !== 'off') setLang(S.lang === 'off' ? CFG.preferred : 'off'); }}
function toggleBar(on) {{
  closeMenus(false);
  document.body.classList.toggle('nobar', !on);
  S.bar = on;
  tell('bar:' + (on ? 1 : 0));
}}
function tick() {{
  if (!player || !player.getDuration) return;
  const d = player.getDuration() || 0, t = player.getCurrentTime() || 0;
  if (!dragging) {{ $('seek').value = d ? t / d * 1000 : 0; $('time').textContent = fmt(t) + ' / ' + fmt(d); }}
}}
function playing(on) {{
  $('play').innerHTML = on ? CFG.icons.pause : CFG.icons.play;
  $('play').title = on ? CFG.labels.pause : CFG.labels.play;
}}
function toggle() {{
  if (!player) return;
  player.getPlayerState() === 1 ? player.pauseVideo() : player.playVideo();
}}
function skip(s) {{ if (player) player.seekTo(Math.max(0, player.getCurrentTime() + s), true); }}
function onYouTubeIframeAPIReady() {{
  player = new YT.Player('yt', {{ events: {{
    onReady: () => {{ youtubeCaptionsOff(); captions(); setInterval(tick, 250); setInterval(subTick, 100); }},
    onStateChange: e => {{ playing(e.data === 1); if (e.data === 1) {{ youtubeCaptionsOff(); tell('playing'); }} }}
  }} }});
}}
const pickers = {{}};
function closeMenus(focus) {{ Object.values(pickers).forEach(p => p.close(focus)); }}
function picker(key, onPick) {{
  const btn = $(key), menu = $(key + '-menu'), opts = [...menu.querySelectorAll('.opt')];
  const p = {{
    value: null,
    set(v) {{
      p.value = v;
      opts.forEach(o => o.setAttribute('aria-selected', String(o.dataset.value === v)));
      const o = opts.find(o => o.dataset.value === v);
      btn.querySelector('.val').textContent = o ? (o.dataset.short || o.textContent) : v;
    }},
    open() {{
      closeMenus(false);
      menu.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      (opts.find(o => o.dataset.value === p.value) || opts[0]).focus();
      tell('menu:1');
    }},
    close(focus) {{
      if (menu.hidden) return;
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      if (focus) btn.focus();
      tell('menu:0');
    }},
  }};
  btn.onclick = e => {{ e.stopPropagation(); menu.hidden ? p.open() : p.close(true); }};
  btn.onkeydown = e => {{
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {{ p.open(); e.preventDefault(); }}
  }};
  opts.forEach((o, i) => {{
    o.onclick = e => {{ e.stopPropagation(); p.set(o.dataset.value); p.close(true); onPick(o.dataset.value); }};
    o.onkeydown = e => {{
      if (e.key === 'ArrowDown') opts[Math.min(opts.length - 1, i + 1)].focus();
      else if (e.key === 'ArrowUp') opts[Math.max(0, i - 1)].focus();
      else if (e.key === 'Home') opts[0].focus();
      else if (e.key === 'End') opts[opts.length - 1].focus();
      else if (e.key === 'Enter' || e.key === ' ') o.click();
      else if (e.key === 'Escape' || e.key === 'Tab') p.close(true);
      else return;
      e.preventDefault();
      e.stopPropagation();
    }};
  }});
  pickers[key] = p;
  return p;
}}
document.addEventListener('click', () => closeMenus(false));
window.addEventListener('blur', () => closeMenus(false));   // videoya (iframe) tıklayınca
picker('speed', v => {{ if (player) player.setPlaybackRate(Number(v)); }}).set('1');
picker('quality', v => tell('q:' + v)).set(S.quality);
picker('cc', setLang).set(S.lang);
captions();
$('play').onclick = toggle;
$('back').onclick = () => skip(-10);
$('fwd').onclick = () => skip(10);
$('seek').oninput = () => {{
  dragging = true;
  const d = player && player.getDuration ? player.getDuration() : 0;
  $('time').textContent = fmt($('seek').value / 1000 * d) + ' / ' + fmt(d);
}};
$('seek').onchange = () => {{
  const d = player && player.getDuration ? player.getDuration() : 0;
  if (player) player.seekTo($('seek').value / 1000 * d, true);
  dragging = false;
}};
$('smaller').onclick = () => {{ S.size = Math.max(-1, S.size - 1); captions(); tell('size:' + S.size); }};
$('larger').onclick = () => {{ S.size = Math.min(3, S.size + 1); captions(); tell('size:' + S.size); }};
$('fs').onclick = () => document.fullscreenElement ? document.exitFullscreen()
                                                    : document.documentElement.requestFullscreen();
$('hidebar').onclick = () => toggleBar(false);
$('showbar').onclick = () => toggleBar(true);
document.body.classList.toggle('nobar', !S.bar);
document.addEventListener('keydown', e => {{
  const el = e.target instanceof Element ? e.target : null;
  if (el && el.closest('.menu')) return;   // açık listede tuşlar listenin
  if (el && el.tagName === 'BUTTON' && (e.key === ' ' || e.key === 'Enter')) return;   // düğmeyi basar
  if (e.key === ' ' || e.key === 'k') {{ toggle(); e.preventDefault(); }}
  else if (e.key === 'ArrowLeft') skip(-5);
  else if (e.key === 'ArrowRight') skip(5);
  else if (e.key === 'f') $('fs').click();
  else if (e.key === 'c') toggleCaptions();
}});
</script>
<script src="https://www.youtube.com/iframe_api"></script>
</body></html>"""


def _reachability() -> bool | None:
    """İnternet var mı? Windows'un ağ bilgisinden; istek atılmıyor.

    `None` bilinmiyor demek: o zaman video yine de deneniyor.
    """
    from PySide6.QtNetwork import QNetworkInformation

    if QNetworkInformation.instance() is None and not QNetworkInformation.loadDefaultBackend():
        return None
    bilgi = QNetworkInformation.instance()
    durum = bilgi.reachability()
    if durum == QNetworkInformation.Reachability.Unknown:
        return None
    return durum == QNetworkInformation.Reachability.Online


class VideoPage(QWebEnginePage):
    """Yalnızca kendi sayfasını ve içindeki oynatıcıyı açan sayfa."""

    def acceptNavigationRequest(  # noqa: N802 (Qt adlandırması)
        self, url: QUrl, kind: QWebEnginePage.NavigationType, is_main_frame: bool
    ) -> bool:
        if not is_main_frame:
            return True
        return url.scheme() in ("data", "about") or url.toString().startswith(BASE_URL)

    def createWindow(self, _kind):  # noqa: N802
        return None

    def javaScriptConsoleMessage(self, *args) -> None:  # noqa: N802
        pass


class VideoView(QWidget):
    """Video sekmesi: oynatıcı ya da internet yok uyarısı, altında atıf."""

    # Tam ekran düğmesi: True girildi, False çıkıldı.
    fullscreen_changed = Signal(bool)

    def __init__(self, language: LanguageManager, parent: QWidget | None = None,
                 online: Callable[[], bool | None] | None = None,
                 settings: tuple[Callable, Callable] | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self._online = online or _reachability
        # (oku, yaz): `ProgressStore.setting` / `set_setting`; yoksa oturumluk.
        oturum: dict = {}
        self._get, self._set = settings or (lambda k, d="": oturum.get(k, d), oturum.__setitem__)
        self._video_id = ""
        self._subtitle_files: dict = {}
        self._credit_text: dict | None = None
        self.loaded_id: str | None = None
        self.paused_by_tab = False
        self._active = False
        self._fullscreen = False
        # Hız ya da kalite listesi açık mı (sayfa `menu:1` / `menu:0` diyor).
        self.menu_open = False
        self._mode = "dark"
        self._web: QWebEngineView | None = None
        self._watching_network = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING["lg"], SPACING["md"], SPACING["lg"], SPACING["md"])
        layout.setSpacing(SPACING["sm"])

        self._stack = QStackedWidget()
        self._stack.setProperty("role", "bare")
        self._player = QWidget()
        self._player.setProperty("role", "bare")
        QVBoxLayout(self._player).setContentsMargins(0, 0, 0, 0)
        self._stack.addWidget(self._player)
        self._stack.addWidget(self._build_offline())
        layout.addWidget(self._stack, 1)

        self._credit = QLabel()
        self._credit.setProperty("role", "muted")
        self._credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._credit.setWordWrap(True)
        self._credit.hide()
        layout.addWidget(self._credit)

        # Altyazı Qt düzeyinde de: videoya tıklanınca tuşlar YouTube'un
        # çerçevesine gidiyor ve sayfanın kendi `c`'si duymuyor. Yalnızca odak
        # video alanındayken; yoksa yan paneldeki not editöründe "c" yazılamazdı.
        kisayol = QShortcut(QKeySequence(Qt.Key.Key_C), self, self.toggle_captions)
        kisayol.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)

    def toggle_captions(self) -> None:
        """Altyazıyı kapatır ya da en son seçilen dile açar (`C`)."""
        if self._web is not None and self.loaded_id is not None:
            self._web.page().runJavaScript("typeof toggleCaptions === 'function' && toggleCaptions()")

    def _build_offline(self) -> QWidget:
        kutu = QWidget()
        kutu.setProperty("role", "bare")
        column = QVBoxLayout(kutu)
        column.setSpacing(SPACING["sm"])
        column.addStretch(1)
        self._offline_icon = QLabel()
        self._offline_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._offline_title = QLabel()
        self._offline_title.setProperty("role", "heading")
        self._offline_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._offline_text = QLabel()
        self._offline_text.setProperty("role", "muted")
        self._offline_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._offline_text.setWordWrap(True)
        self._offline_text.setMaximumWidth(460)
        self._retry = QPushButton()
        self._retry.setCursor(Qt.CursorShape.PointingHandCursor)
        self._retry.clicked.connect(self._try_load)
        for parca in (self._offline_icon, self._offline_title):
            column.addWidget(parca)
        column.addWidget(self._offline_text, 0, Qt.AlignmentFlag.AlignHCenter)
        column.addSpacing(SPACING["sm"])
        column.addWidget(self._retry, 0, Qt.AlignmentFlag.AlignHCenter)
        column.addStretch(1)
        return kutu

    # --- tercihler --------------------------------------------------------

    def prefs(self) -> dict:
        """Saklanan oynatıcı tercihleri (bozuksa varsayılan)."""
        kalite = self._get("video_quality", DEFAULT_PREFS["quality"])
        try:
            boyut = int(self._get("video_caption_size", "0"))
        except ValueError:
            boyut = 0
        dil = self._get("video_caption_lang", "")
        if not dil and self._get("video_captions", "1") == "0":
            dil = "off"   # eski ayar: YouTube altyazısı kapatılmıştı
        return {"lang": dil if dil == "off" or dil in SUBTITLE_LANGS else "",
                "size": boyut if -1 <= boyut <= 3 else 0,
                "quality": kalite if kalite in QUALITIES else DEFAULT_PREFS["quality"],
                "bar": self._get("video_bar", "1") != "0"}

    def _on_title(self, title: str) -> None:
        """Sayfanın mesajı: `q:hd720#3`, `cl:tr#4`, `size:2#5`, `playing#6`.

        Sayfa YouTube'un sayfası değil, bizim sayfamız; yine de yalnızca
        bilinen değerler kabul ediliyor.
        """
        mesaj = title.rsplit("#", 1)[0]
        tur, _, deger = mesaj.partition(":")
        if tur == "q" and deger in QUALITIES:
            self._set("video_quality", deger)
            self._apply_quality()
        elif tur == "cl" and (deger == "off" or deger in SUBTITLE_LANGS):
            self._set("video_caption_lang", deger)
        elif tur == "size" and deger in ("-1", "0", "1", "2", "3"):
            self._set("video_caption_size", deger)
        elif tur == "bar" and deger in ("0", "1"):
            self._set("video_bar", deger)
        elif tur == "menu" and deger in ("0", "1"):
            self.menu_open = deger == "1"
        elif mesaj == "playing":
            self._apply_quality()

    def _apply_quality(self) -> None:
        if self._web is None:
            return
        kalite = self.prefs()["quality"]
        if kalite == "auto":
            return
        for frame in self._web.page().mainFrame().children():
            frame.runJavaScript(QUALITY_JS.format(q=kalite), 0, lambda _r: None)

    # --- içerik -----------------------------------------------------------

    def show_video(self, video_id: str, credit: dict | None, subtitle_files: dict | None = None) -> None:
        """Bölümün videosu; sekme açılınca (`activate`) yükleniyor.

        subtitle_files: {dil: SRT yolu}; dosyalar sayfa kurulurken okunuyor."""
        if video_id != self._video_id:
            self.unload()
        self._video_id = video_id
        self._subtitle_files = dict(subtitle_files or {})
        self._credit_text = credit
        self._render_credit()

    def activate(self) -> None:
        """Video sekmesi öne geldi."""
        self._active = True
        self.paused_by_tab = False
        if self.loaded_id == self._video_id:
            self._stack.setCurrentIndex(0)
            return
        self._try_load()

    def deactivate(self) -> None:
        """Başka sekmeye geçildi: video duraklıyor (sayfa yerinde kalıyor)."""
        self._active = False
        if self.loaded_id is None:
            return
        self.paused_by_tab = True
        self.close_menu()
        if self._web is not None:
            self._web.page().runJavaScript("player && player.pauseVideo && player.pauseVideo()")

    def unload(self) -> None:
        """Bölümden çıkıldı: oynatıcı kapanıyor, ses arkada kalmıyor."""
        self._active = False
        self.paused_by_tab = False
        self.exit_fullscreen()
        if self._web is not None and self.loaded_id is not None:
            self._web.setHtml("", QUrl(BASE_URL))
        self.loaded_id = None
        self.menu_open = False

    def close_menu(self) -> bool:
        """Açık hız/kalite listesini kapatır; kapattıysa True.

        Pencerenin Esc kısayolu tuşu sayfadan önce yakalıyor; liste açıkken
        Esc bölümden çıkarmasın, listeyi kapatsın."""
        if not self.menu_open or self._web is None:
            return False
        self.menu_open = False
        self._web.page().runJavaScript("closeMenus(true)")
        return True

    def exit_fullscreen(self) -> None:
        if self._fullscreen and self._web is not None:
            self._web.page().triggerAction(QWebEnginePage.WebAction.ExitFullScreen)
        self._fullscreen = False

    def offline_visible(self) -> bool:
        return self._stack.currentIndex() == 1

    def _try_load(self) -> None:
        if not self._video_id:
            return
        if self._online() is False:
            self._stack.setCurrentIndex(1)
            self._watch_network()
            return
        self._stack.setCurrentIndex(0)
        self._load_page(self._video_id)
        self.loaded_id = self._video_id

    def _watch_network(self) -> None:
        """Bağlantı gelince uyarıdaki video kendiliğinden açılsın."""
        if self._watching_network:
            return
        from PySide6.QtNetwork import QNetworkInformation

        bilgi = QNetworkInformation.instance()
        if bilgi is not None:
            bilgi.reachabilityChanged.connect(self._reachability_changed)
            self._watching_network = True

    def _reachability_changed(self, *_args) -> None:
        if self._active and self.offline_visible():
            self._try_load()

    def _load_page(self, video_id: str) -> None:
        if self._web is None:
            self._web = QWebEngineView()
            page = VideoPage(profile(), self._web)
            ayarlar = page.settings()
            ayarlar.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
            page.fullScreenRequested.connect(self._on_fullscreen)
            page.titleChanged.connect(self._on_title)
            self._web.setPage(page)
            self._player.layout().addWidget(self._web)
        dil = self._language.language
        profile().setHttpAcceptLanguage("tr-TR,tr;q=0.9,en;q=0.8" if dil == "tr" else "en-US,en;q=0.9")
        self.menu_open = False
        subs = {d: subtitles.load(yol) for d, yol in self._subtitle_files.items() if d in SUBTITLE_LANGS}
        self._web.setHtml(embed_html(video_id, self._language, PALETTES[self._mode], self.prefs(), subs),
                          QUrl(BASE_URL))

    def _on_fullscreen(self, request) -> None:
        request.accept()
        self._fullscreen = request.toggleOn()
        self.fullscreen_changed.emit(self._fullscreen)

    # --- tema ve dil --------------------------------------------------------

    def _render_credit(self) -> None:
        metin = self._language.pick(self._credit_text) if self._credit_text else ""
        self._credit.setText(metin)
        self._credit.setVisible(bool(metin))

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        palette = PALETTES[mode]
        self._offline_icon.setPixmap(icon("globe", palette["text_muted"], 40).pixmap(40, 40))
        if self._web is not None and self.loaded_id is not None:
            degiskenler = {"--bg": "bg", "--surface": "surface", "--hover": "surface_hover",
                           "--border": "border", "--text": "text", "--muted": "text_muted", "--accent": "accent"}
            js = "".join(f"document.documentElement.style.setProperty('{v}', {json.dumps(palette[k])});"
                         for v, k in degiskenler.items())
            self._web.page().runJavaScript(js)

    def retranslate(self) -> None:
        t = self._language.t
        self._offline_title.setText(t("video.offline_title"))
        self._offline_text.setText(t("video.offline_text"))
        self._retry.setText(t("video.retry"))
        self._render_credit()
