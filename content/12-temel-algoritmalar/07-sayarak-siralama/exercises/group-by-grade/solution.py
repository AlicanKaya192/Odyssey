def order_by_grade(records):
    buckets = [[] for _ in range(6)]
    for name, grade in records:
        buckets[grade].append(name)
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


print(order_by_grade([["Ada", 3], ["Bora", 1], ["Cem", 3], ["Deniz", 2]]))
print(order_by_grade([]))
