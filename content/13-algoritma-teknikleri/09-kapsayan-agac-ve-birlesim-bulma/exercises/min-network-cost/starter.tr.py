def min_network_cost(n, roads):
    parent = list(range(n))

    def find(x):
        # Koke kadar cik (yolu kisaltarak).
        return x

    total, taken = 0, 0
    # Ucuzdan pahaliya; kokler farkliysa al.
    return total

roads = [[0, 1, 4], [0, 2, 3], [1, 2, 2], [1, 3, 5],
         [2, 3, 7], [2, 4, 6], [3, 4, 1]]
print(min_network_cost(5, roads))
print(min_network_cost(4, [[0, 1, 1], [2, 3, 1]]))
