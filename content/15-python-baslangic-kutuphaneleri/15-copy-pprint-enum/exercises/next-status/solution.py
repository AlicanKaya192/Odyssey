from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


def next_status(value):
    try:
        current = Status(value)
    except ValueError:
        return "invalid"
    members = list(Status)
    index = members.index(current)
    if index + 1 == len(members):
        return None
    return members[index + 1].value

print(next_status("pending"))
print(next_status("shipped"))
print(next_status("delivered"))
print(next_status("lost"))
