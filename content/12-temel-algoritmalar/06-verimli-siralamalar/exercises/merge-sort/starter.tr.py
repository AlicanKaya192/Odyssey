def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items):
    # Temel durum, bolme, iki yariyi siralayip birlestirme.
    pass


print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
print(merge_sort([]))
