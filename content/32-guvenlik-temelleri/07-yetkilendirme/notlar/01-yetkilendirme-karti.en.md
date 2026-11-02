## Terms

| Term | Meaning |
|---|---|
| **Subject** | Whoever wants to do the job: a user, a program, a service |
| **Object / resource** | The thing the job is done on |
| **Action** | Read, write, delete, approve |
| **Access control matrix** | Rows are subjects, columns objects, cells the allowed actions |
| **ACL** (access control list) | A column of the matrix: next to the object, who may do what |
| **Capability list** | A row of the matrix: next to the subject, what they may do to what |
| **IDOR** | Reaching someone else's object when the object-level check is forgotten |
| **Horizontal abuse** | Reaching another user's data at the same level |
| **Vertical abuse / privilege escalation** | Using a higher privilege |

## The decision sentence

"May the **subject** do the **action** on the **object**?" If there is no
answer: no.

## A Python pattern

```python
def is_allowed(matrix, subject, obj, action):
    return action in matrix.get(subject, {}).get(obj, [])
```

The nested `get` gives a default at every level: an unknown subject and an
unknown object both fall to an empty list, so they are refused.

## Checklist

- Is the decision made on the server?
- Does every endpoint call the same decision function?
- Is the question "whose object is this?" asked?
- Is the role read from the record on the server, not from the client?
- Are refused requests recorded?
