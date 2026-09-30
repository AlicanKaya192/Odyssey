import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("subscribers.csv", index_col="date", parse_dates=True)["subscribers"]
t = np.arange(len(s))
y = s.to_numpy(dtype=float)

single = np.polyfit(t, y, 1)
print(round(float(single[0]), 2))

resid = y - np.polyval(single, t)
top = int(resid.argmax())
print(round(float(resid[0])), round(float(resid[top])), s.index[top].strftime("%m-%d"),
      round(float(resid[-1])))


def line_sse(x, values):
    line = np.polyfit(x, values, 1)
    return float(((values - np.polyval(line, x)) ** 2).sum())


best_k, best_sse = None, None
for k in range(30, len(y) - 30):
    sse = line_sse(t[:k], y[:k]) + line_sse(t[k:], y[k:])
    if best_sse is None or sse < best_sse:
        best_k, best_sse = k, sse

left = np.polyfit(t[:best_k], y[:best_k], 1)
right = np.polyfit(t[best_k:], y[best_k:], 1)
print(s.index[best_k].strftime("%Y-%m-%d"), round(float(left[0]), 2), round(float(right[0]), 2))

ahead = len(y) - 1 + 30
recent = np.polyfit(t[-60:], y[-60:], 1)
print(round(float(np.polyval(single, ahead))), round(float(np.polyval(recent, ahead))))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(s.index, y, color="gray", label="subscribers")
ax.plot(s.index, np.polyval(single, t), linestyle="--", label="single line")
ax.plot(s.index[:best_k], np.polyval(left, t[:best_k]), color="purple", label="two pieces")
ax.plot(s.index[best_k:], np.polyval(right, t[best_k:]), color="purple")
ax.legend()
fig.savefig("chart.png")
