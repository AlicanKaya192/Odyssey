import toolbox

price = 250

final_price = toolbox.with_tax(price)
sale_price = toolbox.discount(price, 10)
rate = toolbox.TAX_RATE

print(final_price)
print(sale_price)
print(rate)
