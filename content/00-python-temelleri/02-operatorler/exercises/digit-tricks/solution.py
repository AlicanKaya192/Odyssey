n = 4827

ones = n % 10
tens = n // 10 % 10
hundreds = n // 100 % 10
thousands = n // 1000

digit_sum = ones + tens + hundreds + thousands
reversed_number = ones * 1000 + tens * 100 + hundreds * 10 + thousands

print("Sum of digits:", digit_sum)
print("Reversed:", reversed_number)
