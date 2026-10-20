def review(old, new):
    # First check whether the code or the data changed, then the model.
    pass


old = {"code": "c1", "data": "d1", "model": "m1"}
print(review(old, {"code": "c1", "data": "d1", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d2", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d1", "model": "m2"}))
print(review(old, {"code": "c2", "data": "d1", "model": "m2"}))
