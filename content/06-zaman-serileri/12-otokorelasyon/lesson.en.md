# Autocorrelation

In Section 06 you asked a question: what do today's sales say about
yesterday's? You measured the answer with two numbers: a correlation of 0.695
with 1 day earlier and 0.958 with 7 days earlier.

This section asks that question **for every lag** and gathers the answer in a
single chart. The correlation of a series with its own past is called
**autocorrelation**; it is the map of the memory of the series. When you build
ARIMA in Section 17, you will decide by reading this map.

## 1. The autocorrelation function (ACF)

For each lag `k`, the correlation of the series with itself `k` steps earlier:

```python
import pandas as pd
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

values = acf(s, nlags=21)
print(values.round(2).tolist())
# [1.0, 0.69, 0.28, 0.11, 0.1, 0.26, 0.67, 0.94, 0.67, 0.26, ...]
```

The first element of the returned array is lag 0 (the correlation of the
series with itself, always 1), then lag 1, 2, 3...

The numbers are very close to what you found with `s.corr(s.shift(k))` but not
identical (lag 7: 0.94 rather than 0.958). `acf` uses the mean and variance of
the **whole** series at every lag; `corr` uses those of the overlapping part at
that lag. `acf` is the standard.

## 2. The correlogram

A bar chart of the ACF values is called a **correlogram**:

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><line class="line" x1="40" y1="172.7" x2="666" y2="172.7"/><text class="dim" x="34" y="176.2" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="103.8" x2="666" y2="103.8"/><text class="dim" x="34" y="107.3" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="34.9" x2="666" y2="34.9"/><text class="dim" x="34" y="38.4" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="214" x2="666" y2="214"/><line class="line" x1="62.2" y1="214" x2="62.2" y2="218"/><text class="dim" x="62.2" y="230" font-size="10.5" text-anchor="middle">0</text><line class="line" x1="256.1" y1="214" x2="256.1" y2="218"/><text class="dim" x="256.1" y="230" font-size="10.5" text-anchor="middle">7</text><line class="line" x1="449.9" y1="214" x2="449.9" y2="218"/><text class="dim" x="449.9" y="230" font-size="10.5" text-anchor="middle">14</text><line class="line" x1="643.8" y1="214" x2="643.8" y2="218"/><text class="dim" x="643.8" y="230" font-size="10.5" text-anchor="middle">21</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="164.5" x2="666" y2="164.5"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="180.8" x2="666" y2="180.8"/><rect class="dot" x="54.5" y="34.9" width="15.3" height="137.8" rx="3" opacity="0.9"/><rect class="dot" x="82.2" y="77.1" width="15.3" height="95.6" rx="3" opacity="0.9"/><rect class="dot" x="109.9" y="134.6" width="15.3" height="38.1" rx="3" opacity="0.9"/><rect class="dot" x="137.6" y="158.1" width="15.3" height="14.6" rx="3" opacity="0.9"/><rect class="dot" x="165.3" y="159.0" width="15.3" height="13.7" rx="3" opacity="0.9"/><rect class="dot" x="193.0" y="136.4" width="15.3" height="36.3" rx="3" opacity="0.9"/><rect class="dot" x="220.7" y="80.5" width="15.3" height="92.2" rx="3" opacity="0.9"/><rect class="dot" x="248.4" y="43.7" width="15.3" height="129.0" rx="3" opacity="0.9"/><rect class="dot" x="276.1" y="80.8" width="15.3" height="91.9" rx="3" opacity="0.9"/><rect class="dot" x="303.8" y="137.2" width="15.3" height="35.5" rx="3" opacity="0.9"/><rect class="dot" x="331.5" y="161.2" width="15.3" height="11.5" rx="3" opacity="0.9"/><rect class="dot" x="359.2" y="161.8" width="15.3" height="10.9" rx="3" opacity="0.9"/><rect class="dot" x="386.9" y="139.3" width="15.3" height="33.4" rx="3" opacity="0.9"/><rect class="dot" x="414.6" y="83.8" width="15.3" height="88.9" rx="3" opacity="0.9"/><rect class="dot" x="442.3" y="47.2" width="15.3" height="125.5" rx="3" opacity="0.9"/><rect class="dot" x="470.0" y="84.0" width="15.3" height="88.7" rx="3" opacity="0.9"/><rect class="dot" x="497.7" y="139.9" width="15.3" height="32.8" rx="3" opacity="0.9"/><rect class="dot" x="525.4" y="163.4" width="15.3" height="9.3" rx="3" opacity="0.9"/><rect class="dot" x="553.1" y="164.0" width="15.3" height="8.7" rx="3" opacity="0.9"/><rect class="dot" x="580.8" y="141.9" width="15.3" height="30.8" rx="3" opacity="0.9"/><rect class="dot" x="608.5" y="87.0" width="15.3" height="85.7" rx="3" opacity="0.9"/><rect class="dot" x="636.2" y="50.8" width="15.3" height="121.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Autocorrelation of the daily sales</text></svg>
  <figcaption>The horizontal axis is the lag (days), the vertical one the correlation. The dashed lines are the confidence band (±0.059). The peaks at lags 7, 14 and 21 are the weekly pattern.</figcaption>
</figure>

statsmodels draws the same chart in one line:

```python
from statsmodels.graphics.tsaplots import plot_acf

fig = plot_acf(s, lags=21)
fig.savefig("chart.png")
```

There are two things on the chart:

**The bars.** The correlation at each lag. In the daily sales, lags 7, 14 and
21 peak: the weekly pattern. The lags in between (3, 4) are almost zero:
Saturday and Tuesday do not resemble each other.

**The confidence band.** Even if the series were completely random, the bars
would not come out exactly zero; they would wobble a little by chance. The
band is the limit of that wobble:

$$\pm \frac{1.96}{\sqrt{n}}$$

For 1096 observations, ±0.059. **A bar inside the band cannot be told from
zero.** A bar outside points to a real relationship. Mind: the band is a 95%
one; even in a random series 1 bar in 20 may stick out.

The shorter the series, the wider the band: ±0.196 for 100 observations. Do
not trust small correlations in a short series.

## 3. Four signatures

The shape of the correlogram tells you what kind of memory the series carries.
There are four basic shapes:

<figure class="fig">
  <svg viewBox="0 0 680 392" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="126.7" x2="316" y2="126.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="140.8" x2="316" y2="140.8"/><rect class="dot" x="47.0" y="34.2" width="7.4" height="99.6" rx="3" opacity="0.9"/><rect class="dot" x="60.4" y="35.4" width="7.4" height="98.4" rx="3" opacity="0.9"/><rect class="dot" x="73.8" y="36.8" width="7.4" height="97.0" rx="3" opacity="0.9"/><rect class="dot" x="87.2" y="38.1" width="7.4" height="95.7" rx="3" opacity="0.9"/><rect class="dot" x="100.6" y="39.5" width="7.4" height="94.3" rx="3" opacity="0.9"/><rect class="dot" x="114.0" y="40.8" width="7.4" height="93.0" rx="3" opacity="0.9"/><rect class="dot" x="127.4" y="42.1" width="7.4" height="91.7" rx="3" opacity="0.9"/><rect class="dot" x="140.8" y="43.5" width="7.4" height="90.3" rx="3" opacity="0.9"/><rect class="dot" x="154.2" y="44.8" width="7.4" height="89.0" rx="3" opacity="0.9"/><rect class="dot" x="167.6" y="46.1" width="7.4" height="87.7" rx="3" opacity="0.9"/><rect class="dot" x="181.0" y="47.4" width="7.4" height="86.4" rx="3" opacity="0.9"/><rect class="dot" x="194.4" y="48.5" width="7.4" height="85.3" rx="3" opacity="0.9"/><rect class="dot" x="207.8" y="49.7" width="7.4" height="84.1" rx="3" opacity="0.9"/><rect class="dot" x="221.2" y="50.8" width="7.4" height="83.0" rx="3" opacity="0.9"/><rect class="dot" x="234.6" y="51.9" width="7.4" height="81.9" rx="3" opacity="0.9"/><rect class="dot" x="248.0" y="52.9" width="7.4" height="80.9" rx="3" opacity="0.9"/><rect class="dot" x="261.4" y="53.9" width="7.4" height="79.9" rx="3" opacity="0.9"/><rect class="dot" x="274.8" y="55.0" width="7.4" height="78.8" rx="3" opacity="0.9"/><rect class="dot" x="288.2" y="56.0" width="7.4" height="77.8" rx="3" opacity="0.9"/><rect class="dot" x="301.6" y="57.1" width="7.4" height="76.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Trend: the price</text></g><g transform="translate(350,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="127.8" x2="316" y2="127.8"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="139.7" x2="316" y2="139.7"/><rect class="dot2" x="47.0" y="63.9" width="7.4" height="69.9" rx="3" opacity="0.9"/><rect class="dot2" x="60.4" y="106.0" width="7.4" height="27.8" rx="3" opacity="0.9"/><rect class="dot2" x="73.8" y="123.1" width="7.4" height="10.7" rx="3" opacity="0.9"/><rect class="dot2" x="87.2" y="123.8" width="7.4" height="10.0" rx="3" opacity="0.9"/><rect class="dot2" x="100.6" y="107.2" width="7.4" height="26.6" rx="3" opacity="0.9"/><rect class="dot2" x="114.0" y="66.4" width="7.4" height="67.4" rx="3" opacity="0.9"/><rect class="dot2" x="127.4" y="39.5" width="7.4" height="94.3" rx="3" opacity="0.9"/><rect class="dot2" x="140.8" y="66.6" width="7.4" height="67.2" rx="3" opacity="0.9"/><rect class="dot2" x="154.2" y="107.9" width="7.4" height="25.9" rx="3" opacity="0.9"/><rect class="dot2" x="167.6" y="125.4" width="7.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="181.0" y="125.8" width="7.4" height="8.0" rx="3" opacity="0.9"/><rect class="dot2" x="194.4" y="109.4" width="7.4" height="24.4" rx="3" opacity="0.9"/><rect class="dot2" x="207.8" y="68.8" width="7.4" height="65.0" rx="3" opacity="0.9"/><rect class="dot2" x="221.2" y="42.1" width="7.4" height="91.7" rx="3" opacity="0.9"/><rect class="dot2" x="234.6" y="69.0" width="7.4" height="64.8" rx="3" opacity="0.9"/><rect class="dot2" x="248.0" y="109.8" width="7.4" height="24.0" rx="3" opacity="0.9"/><rect class="dot2" x="261.4" y="127.0" width="7.4" height="6.8" rx="3" opacity="0.9"/><rect class="dot2" x="274.8" y="127.5" width="7.4" height="6.3" rx="3" opacity="0.9"/><rect class="dot2" x="288.2" y="111.3" width="7.4" height="22.5" rx="3" opacity="0.9"/><rect class="dot2" x="301.6" y="71.1" width="7.4" height="62.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Season: daily sales</text></g><g transform="translate(0,196)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="126.7" x2="316" y2="126.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="140.8" x2="316" y2="140.8"/><rect class="dot" x="47.0" y="129.7" width="7.4" height="4.1" rx="3" opacity="0.9"/><rect class="dot" x="60.4" y="126.3" width="7.4" height="7.5" rx="3" opacity="0.9"/><rect class="dot" x="73.8" y="132.2" width="7.4" height="1.6" rx="3" opacity="0.9"/><rect class="dot" x="87.2" y="129.8" width="7.4" height="4.0" rx="3" opacity="0.9"/><rect class="dot" x="100.6" y="133.8" width="7.4" height="6.2" rx="3" opacity="0.9"/><rect class="dot" x="114.0" y="133.8" width="7.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="127.4" y="132.5" width="7.4" height="1.3" rx="3" opacity="0.9"/><rect class="dot" x="140.8" y="130.1" width="7.4" height="3.7" rx="3" opacity="0.9"/><rect class="dot" x="154.2" y="133.8" width="7.4" height="1.4" rx="3" opacity="0.9"/><rect class="dot" x="167.6" y="133.8" width="7.4" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="181.0" y="133.8" width="7.4" height="5.6" rx="3" opacity="0.9"/><rect class="dot" x="194.4" y="133.8" width="7.4" height="0.1" rx="3" opacity="0.9"/><rect class="dot" x="207.8" y="133.8" width="7.4" height="0.6" rx="3" opacity="0.9"/><rect class="dot" x="221.2" y="133.8" width="7.4" height="5.7" rx="3" opacity="0.9"/><rect class="dot" x="234.6" y="133.4" width="7.4" height="0.4" rx="3" opacity="0.9"/><rect class="dot" x="248.0" y="133.8" width="7.4" height="0.7" rx="3" opacity="0.9"/><rect class="dot" x="261.4" y="131.1" width="7.4" height="2.7" rx="3" opacity="0.9"/><rect class="dot" x="274.8" y="133.8" width="7.4" height="3.0" rx="3" opacity="0.9"/><rect class="dot" x="288.2" y="133.8" width="7.4" height="6.5" rx="3" opacity="0.9"/><rect class="dot" x="301.6" y="133.8" width="7.4" height="2.2" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">White noise: price difference</text></g><g transform="translate(350,196)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="50.7" y1="164" x2="50.7" y2="168"/><text class="dim" x="50.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="104.3" y1="164" x2="104.3" y2="168"/><text class="dim" x="104.3" y="180" font-size="10.5" text-anchor="middle">5</text><line class="line" x1="171.3" y1="164" x2="171.3" y2="168"/><text class="dim" x="171.3" y="180" font-size="10.5" text-anchor="middle">10</text><line class="line" x1="238.3" y1="164" x2="238.3" y2="168"/><text class="dim" x="238.3" y="180" font-size="10.5" text-anchor="middle">15</text><line class="line" x1="305.3" y1="164" x2="305.3" y2="168"/><text class="dim" x="305.3" y="180" font-size="10.5" text-anchor="middle">20</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot2" x="47.0" y="61.1" width="7.4" height="72.7" rx="3" opacity="0.9"/><rect class="dot2" x="60.4" y="82.9" width="7.4" height="50.9" rx="3" opacity="0.9"/><rect class="dot2" x="73.8" y="95.3" width="7.4" height="38.5" rx="3" opacity="0.9"/><rect class="dot2" x="87.2" y="105.7" width="7.4" height="28.1" rx="3" opacity="0.9"/><rect class="dot2" x="100.6" y="114.9" width="7.4" height="18.9" rx="3" opacity="0.9"/><rect class="dot2" x="114.0" y="121.1" width="7.4" height="12.7" rx="3" opacity="0.9"/><rect class="dot2" x="127.4" y="122.6" width="7.4" height="11.2" rx="3" opacity="0.9"/><rect class="dot2" x="140.8" y="122.0" width="7.4" height="11.8" rx="3" opacity="0.9"/><rect class="dot2" x="154.2" y="122.1" width="7.4" height="11.7" rx="3" opacity="0.9"/><rect class="dot2" x="167.6" y="121.9" width="7.4" height="11.9" rx="3" opacity="0.9"/><rect class="dot2" x="181.0" y="122.4" width="7.4" height="11.4" rx="3" opacity="0.9"/><rect class="dot2" x="194.4" y="122.2" width="7.4" height="11.6" rx="3" opacity="0.9"/><rect class="dot2" x="207.8" y="123.0" width="7.4" height="10.8" rx="3" opacity="0.9"/><rect class="dot2" x="221.2" y="123.3" width="7.4" height="10.5" rx="3" opacity="0.9"/><rect class="dot2" x="234.6" y="123.9" width="7.4" height="9.9" rx="3" opacity="0.9"/><rect class="dot2" x="248.0" y="125.4" width="7.4" height="8.4" rx="3" opacity="0.9"/><rect class="dot2" x="261.4" y="124.5" width="7.4" height="9.3" rx="3" opacity="0.9"/><rect class="dot2" x="274.8" y="123.8" width="7.4" height="10.0" rx="3" opacity="0.9"/><rect class="dot2" x="288.2" y="126.8" width="7.4" height="7.0" rx="3" opacity="0.9"/><rect class="dot2" x="301.6" y="128.4" width="7.4" height="5.4" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Short memory: temperature anomaly</text></g></svg>
  <figcaption>The first 20 lags of four series. Each shape is the fingerprint of a different kind of memory.</figcaption>
</figure>

| Shape | Meaning | Example |
|---|---|---|
| Decaying very slowly, all high | Trend: the series is not stationary | Price: 0.99, 0.94, 0.87, 0.76... |
| Peaks at regular intervals | A season | Sales: 7, 14, 21 |
| All inside the band | White noise: no memory | The difference of the price |
| Decaying fast | Short memory | Temperature anomaly: 0.72, 0.51, 0.38... |

## 4. Make it stationary first

The ACF of the price series is still 0.57 at lag 50. That does not mean "the
price remembers 50 days ago"; it only means "the series has a trend". A trend
lifts every lag and hides the real structure underneath.

**Read the ACF on a stationary series** (Section 11). For the seasonal
difference of the daily sales:

```python
d7 = s.diff(7).dropna()
print(acf(d7, nlags=8).round(2).tolist()[1:])
# [0.16, 0.05, 0.13, 0.09, 0.1, 0.03, -0.41, 0.02]
```

The weekly peaks are gone. Two things remain: a small positive at lag 1 (0.16)
and a marked negative at lag 7 (−0.41). These are the real short-term memory of
the series; the model in Section 17 will try to capture exactly these.

## 5. Partial autocorrelation (PACF)

Look at the deviation of the daily temperature from the seasonal normal (how
many degrees that day differs from the average for that calendar day):

```python
t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"]

normal = t.groupby(t.index.dayofyear).transform("mean")
anomaly = t - normal

print(acf(anomaly, nlags=4).round(2).tolist()[1:])
# [0.72, 0.51, 0.38, 0.28]
```

Today has a correlation of 0.72 with yesterday and 0.51 with two days ago. But
do two days ago affect today **directly**, or only through yesterday?

Notice: 0.72 × 0.72 = 0.52. The temperature two days ago affected yesterday,
and yesterday affected today. The whole of the 0.51 may come from this
**chain**.

**Partial autocorrelation** answers exactly this question: the **direct**
contribution of lag `k` once the effect of the lags in between is removed.

```python
from statsmodels.tsa.stattools import pacf

print(pacf(anomaly, nlags=4).round(2).tolist()[1:])
# [0.72, -0.03, 0.06, -0.02]
```

<figure class="fig">
  <svg viewBox="0 0 680 190" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="60.8" y1="164" x2="60.8" y2="168"/><text class="dim" x="60.8" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="86.9" y1="164" x2="86.9" y2="168"/><text class="dim" x="86.9" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="138.9" y1="164" x2="138.9" y2="168"/><text class="dim" x="138.9" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="191.0" y1="164" x2="191.0" y2="168"/><text class="dim" x="191.0" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="243.1" y1="164" x2="243.1" y2="168"/><text class="dim" x="243.1" y="180" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="295.2" y1="164" x2="295.2" y2="168"/><text class="dim" x="295.2" y="180" font-size="10.5" text-anchor="middle">10</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot" x="53.7" y="61.1" width="14.3" height="72.7" rx="3" opacity="0.9"/><rect class="dot" x="79.7" y="82.9" width="14.3" height="50.9" rx="3" opacity="0.9"/><rect class="dot" x="105.7" y="95.3" width="14.4" height="38.5" rx="3" opacity="0.9"/><rect class="dot" x="131.8" y="105.7" width="14.3" height="28.1" rx="3" opacity="0.9"/><rect class="dot" x="157.8" y="114.9" width="14.3" height="18.9" rx="3" opacity="0.9"/><rect class="dot" x="183.9" y="121.1" width="14.3" height="12.7" rx="3" opacity="0.9"/><rect class="dot" x="209.9" y="122.6" width="14.3" height="11.2" rx="3" opacity="0.9"/><rect class="dot" x="235.9" y="122.0" width="14.4" height="11.8" rx="3" opacity="0.9"/><rect class="dot" x="262.0" y="122.1" width="14.3" height="11.7" rx="3" opacity="0.9"/><rect class="dot" x="288.0" y="121.9" width="14.3" height="11.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">ACF: the total relationship</text></g><g transform="translate(350,0)"><line class="line" x1="40" y1="133.8" x2="316" y2="133.8"/><text class="dim" x="34" y="137.3" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="83.4" x2="316" y2="83.4"/><text class="dim" x="34" y="86.9" font-size="10.5" text-anchor="end">0.5</text><line class="grid" x1="40" y1="33.0" x2="316" y2="33.0"/><text class="dim" x="34" y="36.5" font-size="10.5" text-anchor="end">1</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="60.8" y1="164" x2="60.8" y2="168"/><text class="dim" x="60.8" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="86.9" y1="164" x2="86.9" y2="168"/><text class="dim" x="86.9" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="138.9" y1="164" x2="138.9" y2="168"/><text class="dim" x="138.9" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="191.0" y1="164" x2="191.0" y2="168"/><text class="dim" x="191.0" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="243.1" y1="164" x2="243.1" y2="168"/><text class="dim" x="243.1" y="180" font-size="10.5" text-anchor="middle">8</text><line class="line" x1="295.2" y1="164" x2="295.2" y2="168"/><text class="dim" x="295.2" y="180" font-size="10.5" text-anchor="middle">10</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="129.6" x2="316" y2="129.6"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="138.0" x2="316" y2="138.0"/><rect class="dot2" x="53.7" y="61.0" width="14.3" height="72.8" rx="3" opacity="0.9"/><rect class="dot2" x="79.7" y="133.8" width="14.3" height="3.2" rx="3" opacity="0.9"/><rect class="dot2" x="105.7" y="127.9" width="14.4" height="5.9" rx="3" opacity="0.9"/><rect class="dot2" x="131.8" y="133.8" width="14.3" height="2.1" rx="3" opacity="0.9"/><rect class="dot2" x="157.8" y="133.8" width="14.3" height="3.1" rx="3" opacity="0.9"/><rect class="dot2" x="183.9" y="133.7" width="14.3" height="0.1" rx="3" opacity="0.9"/><rect class="dot2" x="209.9" y="128.5" width="14.3" height="5.3" rx="3" opacity="0.9"/><rect class="dot2" x="235.9" y="129.0" width="14.4" height="4.8" rx="3" opacity="0.9"/><rect class="dot2" x="262.0" y="132.4" width="14.3" height="1.4" rx="3" opacity="0.9"/><rect class="dot2" x="288.0" y="131.1" width="14.3" height="2.7" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">PACF: the direct contribution</text></g></svg>
  <figcaption>The temperature anomaly. The ACF fades step by step; the PACF has only lag 1. The long tail is the echo of a single direct link.</figcaption>
</figure>

The direct contribution of the second lag is −0.03: nothing. To forecast today
it is enough to know yesterday; two days ago carries no extra information. The
long tail in the ACF is only the echo of yesterday's effect.

An analogy: a rumour travels from ear to ear. What was said three people back
resembles what you heard (ACF), but you only heard it from the person next to
you (PACF).

To plot it: `plot_pacf(anomaly, lags=20)`.

## 6. Two basic processes: AR and MA

The short memory of stationary series comes in two basic forms.

**AR (autoregressive):** today is a multiple of yesterday plus a new shock.

$$y_t = 0.7\, y_{t-1} + e_t$$

The effect of a shock fades, multiplied by 0.7 each day: a long but weakening
echo. The temperature anomaly is exactly such a series.

**MA (moving average):** today is today's shock plus a multiple of yesterday's
shock.

$$y_t = e_t + 0.7\, e_{t-1}$$

The shock is felt for just one more day and then vanishes completely: a short,
sharp echo. (The name has nothing to do with the moving average of Section 07.)

Their correlograms are **mirror images of each other**:

<figure class="fig">
  <svg viewBox="0 0 680 392" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot" x="56.8" y="48.6" width="17.7" height="66.8" rx="3" opacity="0.9"/><rect class="dot" x="88.9" y="70.3" width="17.7" height="45.1" rx="3" opacity="0.9"/><rect class="dot" x="121.0" y="84.7" width="17.7" height="30.7" rx="3" opacity="0.9"/><rect class="dot" x="153.1" y="92.7" width="17.7" height="22.7" rx="3" opacity="0.9"/><rect class="dot" x="185.2" y="97.6" width="17.7" height="17.8" rx="3" opacity="0.9"/><rect class="dot" x="217.3" y="98.0" width="17.7" height="17.4" rx="3" opacity="0.9"/><rect class="dot" x="249.4" y="99.7" width="17.7" height="15.7" rx="3" opacity="0.9"/><rect class="dot" x="281.5" y="103.5" width="17.7" height="11.9" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">AR(1) · ACF</text></g><g transform="translate(350,0)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot2" x="56.8" y="48.5" width="17.7" height="66.9" rx="3" opacity="0.9"/><rect class="dot2" x="88.9" y="115.4" width="17.7" height="1.7" rx="3" opacity="0.9"/><rect class="dot2" x="121.0" y="114.8" width="17.7" height="0.6" rx="3" opacity="0.9"/><rect class="dot2" x="153.1" y="112.1" width="17.7" height="3.3" rx="3" opacity="0.9"/><rect class="dot2" x="185.2" y="113.3" width="17.7" height="2.1" rx="3" opacity="0.9"/><rect class="dot2" x="217.3" y="108.5" width="17.7" height="6.9" rx="3" opacity="0.9"/><rect class="dot2" x="249.4" y="114.8" width="17.7" height="0.6" rx="3" opacity="0.9"/><rect class="dot2" x="281.5" y="115.4" width="17.7" height="2.8" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">AR(1) · PACF</text></g><g transform="translate(0,196)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot" x="56.8" y="71.0" width="17.7" height="44.4" rx="3" opacity="0.9"/><rect class="dot" x="88.9" y="115.4" width="17.7" height="3.6" rx="3" opacity="0.9"/><rect class="dot" x="121.0" y="115.4" width="17.7" height="4.3" rx="3" opacity="0.9"/><rect class="dot" x="153.1" y="115.4" width="17.7" height="3.1" rx="3" opacity="0.9"/><rect class="dot" x="185.2" y="115.4" width="17.7" height="0.8" rx="3" opacity="0.9"/><rect class="dot" x="217.3" y="109.6" width="17.7" height="5.8" rx="3" opacity="0.9"/><rect class="dot" x="249.4" y="109.2" width="17.7" height="6.2" rx="3" opacity="0.9"/><rect class="dot" x="281.5" y="112.6" width="17.7" height="2.8" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">MA(1) · ACF</text></g><g transform="translate(350,196)"><line class="grid" x1="40" y1="164.0" x2="316" y2="164.0"/><text class="dim" x="34" y="167.5" font-size="10.5" text-anchor="end">−0.5</text><line class="line" x1="40" y1="115.4" x2="316" y2="115.4"/><text class="dim" x="34" y="118.9" font-size="10.5" text-anchor="end">0</text><line class="grid" x1="40" y1="66.9" x2="316" y2="66.9"/><text class="dim" x="34" y="70.4" font-size="10.5" text-anchor="end">0.5</text><line class="line" x1="40" y1="164" x2="316" y2="164"/><line class="line" x1="65.7" y1="164" x2="65.7" y2="168"/><text class="dim" x="65.7" y="180" font-size="10.5" text-anchor="middle">1</text><line class="line" x1="97.8" y1="164" x2="97.8" y2="168"/><text class="dim" x="97.8" y="180" font-size="10.5" text-anchor="middle">2</text><line class="line" x1="162.0" y1="164" x2="162.0" y2="168"/><text class="dim" x="162.0" y="180" font-size="10.5" text-anchor="middle">4</text><line class="line" x1="226.1" y1="164" x2="226.1" y2="168"/><text class="dim" x="226.1" y="180" font-size="10.5" text-anchor="middle">6</text><line class="line" x1="290.3" y1="164" x2="290.3" y2="168"/><text class="dim" x="290.3" y="180" font-size="10.5" text-anchor="middle">8</text><line class="curve3" stroke-dasharray="4 4" x1="40" y1="107.7" x2="316" y2="107.7"/><line class="curve3" stroke-dasharray="4 4" x1="40" y1="123.2" x2="316" y2="123.2"/><rect class="dot2" x="56.8" y="70.9" width="17.7" height="44.5" rx="3" opacity="0.9"/><rect class="dot2" x="88.9" y="115.4" width="17.7" height="30.4" rx="3" opacity="0.9"/><rect class="dot2" x="121.0" y="98.8" width="17.7" height="16.6" rx="3" opacity="0.9"/><rect class="dot2" x="153.1" y="115.4" width="17.7" height="13.7" rx="3" opacity="0.9"/><rect class="dot2" x="185.2" y="105.8" width="17.7" height="9.6" rx="3" opacity="0.9"/><rect class="dot2" x="217.3" y="113.9" width="17.7" height="1.5" rx="3" opacity="0.9"/><rect class="dot2" x="249.4" y="113.0" width="17.7" height="2.4" rx="3" opacity="0.9"/><rect class="dot2" x="281.5" y="115.0" width="17.7" height="0.4" rx="3" opacity="0.9"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">MA(1) · PACF</text></g></svg>
  <figcaption>The top row is AR(1), the bottom row MA(1); both with a coefficient of 0.7 and 600 observations. In AR the ACF decays and the PACF cuts off; in MA it is the other way round.</figcaption>
</figure>

<figure class="fig">
<div class="versus">
<div><h4>AR(1)</h4><p>ACF: <b>decays slowly</b> (0.69, 0.46, 0.32, 0.23).</p><p>PACF: <b>cuts off</b> after lag 1 (0.69, −0.02, 0.01).</p></div>
<div><h4>MA(1)</h4><p>ACF: <b>cuts off</b> after lag 1 (0.46, −0.04, −0.04).</p><p>PACF: <b>decays slowly</b>, changing sign (0.46, −0.31, 0.17).</p></div>
</div>
<figcaption>The chart that cuts off gives the order: if the PACF cuts off after lag 2 it is AR(2); if the ACF cuts off after lag 3 it is MA(3).</figcaption>
</figure>

For now it is enough to recognise these two shapes. In Section 17 you will
read the `p` and `q` of ARIMA off exactly these charts.

## 7. Is any memory left? The Ljung–Box test

Instead of looking at 20 bars one by one, a single question: **are the first m
lags all zero at once?**

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(acorr_ljungbox(k.diff().dropna(), lags=[10]))
#       lb_stat  lb_pvalue
# 10     12.026      0.283
```

The assumption of the test is "the series is white noise". p = 0.283: it cannot
be rejected. In the daily change of the price no usable memory shows in the
first 10 lags; consistent with the random walk diagnosis (Section 11).

```python
print(acorr_ljungbox(d7, lags=[14]))
#       lb_stat  lb_pvalue
# 14    261.782        0.0
```

For the seasonal difference of the sales p = 0.000: there is still structure
in it that can be modelled.

The real job of this test is **model checking**. After fitting a model you
apply it to the residual: if p is large the model took all of the memory; if
small, there is still information in the residual and the model is incomplete.
The residuals of the decompositions in Section 10 fail this test (p = 0.000):
a decomposition takes the trend and the season, not the short-term memory.
Taking that is the job of ARIMA.

## 8. Finding the period

If you do not know the length of the season, the ACF tells you. For the hourly
electricity load:

```python
load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)
load = load["load_mw"]

values = acf(load, nlags=200)
print(values[[12, 24, 48, 168]].round(2).tolist())
# [-0.47, 0.88, 0.77, 0.87]
```

12 hours later goes the **opposite** way (day and night), 24 hours later is
0.88 (the same hour), 168 hours later 0.87 (the same hour, the same day).
There are two periods: 24 and 168. This is the reason for writing
`MSTL(periods=(24, 168))` in Section 10.

## Common mistakes

| Mistake | Result | The right way |
|---|---|---|
| Reading the ACF of a trending series | Every lag is high; no structure shows | Make it stationary first |
| Interpreting a bar inside the band | Reading meaning into noise | Look only at those beyond the band |
| Reading meaning into one distant lag beyond the band | 1 in 20 sticks out by chance | Is it a sensible lag (7, 12, 24)? |
| Mixing up ACF and PACF | The wrong model order | ACF: the total relationship. PACF: the direct contribution |
| Forgetting lag 0 in the `acf` array | Reading shifted by one | `values[k]` is lag `k`; `values[0]` is always 1 |
| Calling it with `NaN` in the series | The result is `NaN` | `dropna()` |
| Many lags on a short series | A wide band, unreliable values | At most `n / 4` lags |
| Taking a large Ljung–Box p for "the model is right" | Overconfidence | It means "no remaining memory was found" |

## Summary

- **Autocorrelation**: the correlation of a series with its own lag. The
  **ACF** gives every lag; its chart is the **correlogram**.
- The **confidence band** ±1.96/√n: a bar inside it cannot be told from zero.
- Four signatures: slow decay (trend), regular peaks (season), all in the band
  (white noise), fast decay (short memory).
- Read the ACF on a **stationary** series.
- **PACF**: the direct contribution once the effect of the lags in between is
  removed.
- **AR**: the ACF decays, the PACF cuts off. **MA**: the ACF cuts off, the
  PACF decays.
- **Ljung–Box**: "are the first m lags zero at once"; the standard test for
  checking residuals.

You can now get to know a series: its components, its stationarity, its
memory. One last preparation remains before forecasting: real data arrives
incomplete and dirty. Section 13 deals with missing data and outliers.
