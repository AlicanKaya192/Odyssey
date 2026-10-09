class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build_linked(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.value)
        head = head.next
    return out


def append_value(head, value):
    new = Node(value)
    # Bos liste mi? Degilse son dugume git.

    return head

def append_to(values, value):
    return to_list(append_value(build_linked(values), value))

print(append_to([1, 2, 3], 4))
print(append_to([], 9))
