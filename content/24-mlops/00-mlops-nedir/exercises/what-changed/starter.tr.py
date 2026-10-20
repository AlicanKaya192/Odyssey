def review(old, new):
    # Once kod ya da verinin, sonra modelin degisip degismedigine bak.
    pass


old = {"code": "c1", "data": "d1", "model": "m1"}
print(review(old, {"code": "c1", "data": "d1", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d2", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d1", "model": "m2"}))
print(review(old, {"code": "c2", "data": "d1", "model": "m2"}))
