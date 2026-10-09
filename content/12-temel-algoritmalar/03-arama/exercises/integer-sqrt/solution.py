def integer_sqrt(n):
    lo, hi = 0, n
    answer = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            answer = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return answer


for n in [0, 1, 15, 16, 50, 99]:
    print(n, integer_sqrt(n))
print(integer_sqrt(10**12 + 7))
