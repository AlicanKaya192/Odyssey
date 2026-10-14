def step_status(code):
    # Cikis koduna gore metni dondur.
    pass


def pipeline_status(codes):
    # Ilk sifir olmayan adimda dur; step_status'u kullan.
    pass


print(step_status(0))
print(step_status(1))
print(step_status(5))
print(step_status(2))
print(pipeline_status([0, 0, 0]))
print(pipeline_status([0, 1, 0]))
print(pipeline_status([0, 0, 5]))
