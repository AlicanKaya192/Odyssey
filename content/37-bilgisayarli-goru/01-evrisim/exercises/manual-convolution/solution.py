def convolve(img, kernel):
    kh, kw = len(kernel), len(kernel[0])
    out = []
    for r in range(len(img) - kh + 1):
        row = []
        for c in range(len(img[0]) - kw + 1):
            total = 0
            for i in range(kh):
                for j in range(kw):
                    total += img[r + i][c + j] * kernel[i][j]
            row.append(total)
        out.append(row)
    return out

img = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(convolve(img, [[1, 0], [0, -1]]))
print(convolve(img, [[1, 1, 1]]))
