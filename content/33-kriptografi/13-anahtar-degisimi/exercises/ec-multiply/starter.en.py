P, A = 97, 1


def add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        s = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P
    else:
        s = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return [x3, y3]


def mul(k, pt):
    result = None
    while k > 0:
        if k & 1:
            result = add(result, pt)
        k >>= 1
    return result

G = [0, 2]
print(mul(1, G))
print(mul(2, G) == add(G, G))
print(mul(13, mul(29, G)) == mul(29, mul(13, G)))
print(mul(89, G))
