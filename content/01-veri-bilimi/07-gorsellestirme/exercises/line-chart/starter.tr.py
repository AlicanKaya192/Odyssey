import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Bursa", "Adana"],
    "score": [87, 71, 69, 78],
    "hours": [12, 6, 5, 9],
})

months = ["Jan", "Feb", "Mar", "Apr"]
sales = [120, 150, 130, 180]

# Aylari x, satislari y ekseninde gosteren cizgi grafigi ciz.
# Noktalari marker="o" ile isaretle.


# Basligi ve y eksen etiketini ayarla.


# Cizgi sayisi, cizginin y verisi ve y etiketini yazdir.
