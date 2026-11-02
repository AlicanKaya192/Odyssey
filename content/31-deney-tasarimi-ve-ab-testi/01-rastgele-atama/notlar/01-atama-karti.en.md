## The bucket function

```python
import hashlib


def bucket(user_id, salt):
    digest = hashlib.md5(f"{salt}:{user_id}".encode()).hexdigest()
    return int(digest, 16) % 100


def assign(user_id, salt, share_b=50):
    return "B" if bucket(user_id, salt) < share_b else "A"


print(assign("U00001", "checkout-v2"), assign("U00001", "checkout-v2"))
print(assign("U00001", "checkout-v2", share_b=10))
```

```text
B B
A
```

- Same id + same salt → always the same group.
- `share_b` is the bucket threshold: with 10, about 10% of users see B.
- Raising the share later (10 → 50) keeps the old B users in B and adds new
  ones; but if the share changes in the middle of the test, the days get
  mixed. The share is chosen at the start.

## The balance table

After assignment, look at traits the change cannot affect: platform share,
earlier visit counts, country, new or returning user. If the groups differ
a lot, look for a bug in the assignment.

## Don't

- Assign with `hash()`: for strings it changes on every run.
- Give every experiment the same salt: the experiments get locked together.
- Compare those who turned on an opt-in feature with those who did not and
  claim an effect.
- Assign by user and then count every page view as a separate observation.
