def rate_limit(times, capacity, rate):
    tokens = capacity
    last = 0
    result = ""
    for now in times:
        tokens = min(capacity, tokens + (now - last) * rate)
        last = now
        if tokens >= 1:
            tokens -= 1
            result += "+"
        else:
            result += "-"
    return result

print(rate_limit([0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3], 3, 1))
print(rate_limit([0, 0, 0, 10, 10, 10, 10], 2, 1))
