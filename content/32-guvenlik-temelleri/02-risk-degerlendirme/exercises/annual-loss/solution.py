def ale(asset_value, exposure_factor, aro):
    sle = asset_value * exposure_factor
    return round(sle * aro, 2)

print(ale(500000, 0.4, 0.1))
print(ale(1200, 1.0, 3))
print(ale(80000, 0.25, 0.5))
