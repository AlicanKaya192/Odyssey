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


def length(head):
    count = 0
    # Dugumleri gez, say.

    return count

def length_of(values):
    return length(build_linked(values))

print(length_of([4, 8, 15, 16, 23, 42]))
print(length_of([]))
