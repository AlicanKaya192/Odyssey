import numpy as np

flat = np.array([12, 15, 9, 20, 18, 11, 14, 17, 13])
matrix = flat.reshape(3, 3)

per_student = matrix.sum(axis=1)
per_exam = matrix.mean(axis=0)
best = per_student.argmax()

print(matrix)
print(per_student)
print(np.round(per_exam, 2))
print(best)
