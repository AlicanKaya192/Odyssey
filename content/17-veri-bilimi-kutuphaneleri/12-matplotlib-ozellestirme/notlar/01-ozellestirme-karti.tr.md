## Eksen

| Yazım | Ne yapar |
|---|---|
| `ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))` | binlik ayraç |
| `ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))` | 0,18 → 18% |
| `ax.set_yscale("log")` | logaritmik eksen |
| `ax.set_xlim(0, 10)` / `ax.invert_yaxis()` | sınır / ters çevir |
| `ax.tick_params(axis="x", rotation=45)` | işaret yazılarını döndür |
| `ax.xaxis.set_major_locator(mdates.MonthLocator())` | her ay bir işaret |
| `ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))` | tarih biçimi |
| `ax2 = ax.twinx()` | sağda ikinci y ekseni |

## Not ve vurgu

| Yazım | Ne yapar |
|---|---|
| `ax.annotate("t", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="->"))` | oklu not |
| `ax.axhline(y)` / `ax.axvline(x)` | referans çizgisi |
| `ax.axvspan(x1, x2, alpha=0.2)` | aralığı boya |
| `ax.bar_label(bars, padding=3)` | çubuğa değer yaz |
| `bars[i].set_color("tab:blue")` | tek çubuğu vurgula |
| `ax.spines[["top", "right"]].set_visible(False)` | çerçeveyi kaldır |
| `ax.legend(loc="upper left", frameon=False)` | açıklama yeri |

## Genel ayar

| Yazım | Kapsam |
|---|---|
| `with plt.rc_context({...}):` | yalnızca blok |
| `plt.rcParams["font.size"] = 11` | betiğin geri kalanı |
| `plt.style.use("tableau-colorblind10")` | betiğin geri kalanı |
| `with plt.style.context("ggplot"):` | yalnızca blok |

## Kontrol listesi

- Başlık mesajı söylüyor mu ("A, B'den %20 fazla")?
- Eksen adlarında birim var mı?
- Sayılar okunur mu (`1e6` değil `1,250,000`)?
- Tek bir vurgu rengi mi var?
- Renk olmadan da anlaşılıyor mu (işaret, etiket)?
- Çubuk ekseni sıfırdan mı başlıyor; log eksen söylendi mi?
