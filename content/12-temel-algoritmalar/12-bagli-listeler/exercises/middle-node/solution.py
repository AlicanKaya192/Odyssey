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


def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.value if slow else None

def middle_of(values):
    return middle(build_linked(values))

print(middle_of([1, 2, 3, 4, 5]))
print(middle_of([1, 2, 3, 4]))
print(middle_of([]))
