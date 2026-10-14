def history_cost(tokens, price_in, price_out):
    total_in, sent = 0, 0
    for t in tokens:
        sent += t
        total_in += sent
    total_out = 20 * len(tokens)
    cost = (total_in * price_in + total_out * price_out) / 1_000_000
    return [total_in, round(cost, 6)]


print(history_cost([10, 8, 12, 6], 0.5, 1.5))
