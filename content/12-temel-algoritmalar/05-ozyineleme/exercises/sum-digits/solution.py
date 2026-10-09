def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)


print(sum_digits(1234))
print(sum_digits(7))
print(sum_digits(99999))
