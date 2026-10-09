def stock_span(prices):
    spans = []
    stack = []
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] <= p:
            stack.pop()
        spans.append(i - stack[-1] if stack else i + 1)
        stack.append(i)
    return spans

print(stock_span([100, 80, 60, 70, 60, 75, 85]))
rising = list(range(100_000))
print(stock_span(rising)[-1])
