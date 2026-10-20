def review(old, new):
    inputs_changed = old["code"] != new["code"] or old["data"] != new["data"]
    model_changed = old["model"] != new["model"]
    if not inputs_changed and not model_changed:
        return "nothing"
    if inputs_changed and not model_changed:
        return "retrain"
    if model_changed and not inputs_changed:
        return "unknown model"
    return "ok"


old = {"code": "c1", "data": "d1", "model": "m1"}
print(review(old, {"code": "c1", "data": "d1", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d2", "model": "m1"}))
print(review(old, {"code": "c1", "data": "d1", "model": "m2"}))
print(review(old, {"code": "c2", "data": "d1", "model": "m2"}))
