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


def reverse(head):
    prev = None
    # Sakla, cevir, ilerle.

    return prev

def reverse_values(values):
    return to_list(reverse(build_linked(values)))

print(reverse_values([1, 2, 3, 4]))
print(reverse_values([]))
