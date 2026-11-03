import numpy as np
from ab_data import make_segment_test

keys = ["country", "platform", "group"]
# make_segment_test(n=20000, seed=s) ile s = 500..549 arası 50 test kur.
# Her testte toplam göreli artışı ve 16 segmentin en büyük artışını bul.
# Önce toplam artışların, sonra en büyük segment artışlarının ortalamasını
# 3 basamakla yaz. (Gerçek etki her segmentte 0.08.)
