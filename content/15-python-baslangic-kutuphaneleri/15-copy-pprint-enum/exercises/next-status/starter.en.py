from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


def next_status(value):
    # Status(value) raises ValueError if invalid
    return None

print(next_status("pending"))
print(next_status("shipped"))
print(next_status("delivered"))
print(next_status("lost"))
