def rto_check(size_gb, speed, setup, rto):
    hours = size_gb / speed
    return [round(hours, 1), hours <= rto]

print(rto_check(900, 150, 1.5, 6))
print(rto_check(400, 200, 0.5, 4))
