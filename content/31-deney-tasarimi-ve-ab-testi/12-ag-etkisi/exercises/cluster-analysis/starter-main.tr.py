from scipy import stats
from ab_data import make_market

cities = make_market(seed=22, design="city")
# 1) Şehir ortalamalarıyla (her şehir bir gözlem) Welch p'sini 3 basamakla
#    yaz.
# 2) Aynı veride kullanıcıları bağımsız sayan Welch p'sini yaz.
