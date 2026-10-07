# prefix /orders, tags ["orders"], every endpoint requires require_key (deps.py)
# POST /orders/{item}: raise OutOfStock(item) if out of stock; otherwise decrease by one, {"item", "left"}
