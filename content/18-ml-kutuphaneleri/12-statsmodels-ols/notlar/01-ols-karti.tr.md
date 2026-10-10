## Kurmak

| Yazım | Ne yapar |
|---|---|
| `import statsmodels.api as sm` | dizi arayüzü |
| `sm.add_constant(X)` | `const` sütunu ekler (unutma) |
| `sm.add_constant(new, has_constant="add")` | tek satırda da ekler |
| `sm.OLS(y, X).fit()` | modeli eğitir |
| `.fit(cov_type="HC3")` | sabit olmayan varyansa dayanıklı standart hata |

## Sonuç nesnesi

| Nitelik | Ne |
|---|---|
| `res.params` | katsayılar |
| `res.bse` | standart hatalar |
| `res.pvalues` | p-değerleri |
| `res.conf_int(alpha=0.05)` | güven aralıkları |
| `res.rsquared`, `res.rsquared_adj` | R² ve düzeltilmiş R² |
| `res.aic`, `res.bic` | model karşılaştırma (küçük iyi) |
| `res.resid`, `res.fittedvalues` | artıklar, uydurulan değerler |
| `res.summary()`, `res.summary().tables[1]` | rapor, katsayı tablosu |
| `res.get_prediction(X_new).summary_frame()` | tahmin, `mean_ci`, `obs_ci` |

## Tanılar

| Yazım | Sorusu |
|---|---|
| `variance_inflation_factor(X.values, i)` | bu sütun başkalarıyla aynı mı? (10+ kötü) |
| `het_breuschpagan(res.resid, res.model.exog)` | hata varyansı sabit mi? (küçük p: değil) |
| `res.f_test("x = 0")` | bir ya da birkaç katsayı sıfır mı? |

## Okurken

- p-değeri etkinin **büyüklüğü** değil; büyük veride küçük bir etki de çok
  küçük p alır. Önce katsayıya ve aralığına bak.
- Büyük p "etki yok" değil, "bu veriyle ayırt edilemiyor".
- Gözlemsel veride katsayı **neden-sonuç** değil, ilişki söyler.
