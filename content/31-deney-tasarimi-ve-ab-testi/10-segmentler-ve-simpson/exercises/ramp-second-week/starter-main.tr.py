from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_ramp_test

ramp = make_ramp_test(seed=11)
# 1) Toplam satın alma oranlarını yaz (önce A, sonra B; 4 basamak).
# 2) Yalnızca ikinci haftanın (week == 2) oranlarını aynı biçimde yaz.
# 3) İkinci hafta için iki oran z-testinin p'sini 3 basamakla yaz
#    (proportions_ztest, önce B sonra A).
