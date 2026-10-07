import pandas as pd
from orders_data import make_orders

df = make_orders(100_000)

# For three columns: name, smallest, largest, downcast type.
