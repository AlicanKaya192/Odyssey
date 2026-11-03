## Types

| Type | Example | What is missing |
|---|---|---|
| Horizontal | Seeing another customer's invoice | An ownership check |
| Vertical | An ordinary user doing an admin operation | A role check |

## Cause → prevention

| Cause | Prevention |
|---|---|
| An object is fetched by number without looking at its owner | `invoice["owner"] == user` on every request |
| Every field in the request is written to the record (mass assignment) | An allow list: `if key in ALLOWED` |
| A privileged task's script can be written by others | The script belongs to the admin account, `mode & 0o022 == 0` |
| An unexpected setuid program | A setuid allow list, a regular inventory |
| Unpatched software | Patch management |
| A common or shared admin password | Personal accounts, least privilege |

## Detection signs

- Privilege requests from the same user refused several times in a short
  time.
- A new member being added to the administrators group.
- A newly appearing setuid file or a new scheduled task.
- Admin operations an ordinary account has never done before.

## Python patterns

- The setuid bit: `mode & stat.S_ISUID` (`0o4000`).
- Can the group or others write: `mode & 0o022`.
- Turning `key=value` fields into a dict: `dict(p.split("=") for p in parts)`.
- Counting: `collections.Counter`; threshold: `count >= threshold`.
- The difference between two snapshots: `set(after) - set(before)`.

## Keep in mind

- Being authenticated is not the same as being able to reach every object.
- Saying "not found" for someone else's object also hides which objects
  exist.
- Role and privilege fields do not change through data from the client.
