## Security review checklist

| Topic | Question to ask |
|---|---|
| Input | Is every piece of outside data validated with an allow list? |
| Output | Is data encoded or parameterised when it goes into HTML, SQL or a command? |
| Identity | Does the endpoint require login? |
| Authorization | Are ownership and role checked on the server on every request? |
| Errors | Does the check refuse on an error; does the error message leak internals? |
| Secrets | Is there a password, key or token in code, configuration or logs? |
| Crypto | No home-made encryption; a trusted library, the right mode |
| Dependencies | Is the new package needed, is its version pinned? |
| Removals | Does the change remove a check, a test or a log entry? |

## Good review habits

- Ask for small changes: a thousand-line diff is not really read.
- Read the removed lines first.
- Ask "why is this safe?"; the answer should be in the code or the
  description.
- Write the finding about the code, not the person; the goal is the bug,
  not someone to blame.

## AST patterns

| Looking for | Node |
|---|---|
| A function call | `ast.Call`, name `node.func.id` |
| A method call | `ast.Call`, `node.func` is an `ast.Attribute` |
| An assignment | `ast.Assign`, targets `node.targets` |
| A constant value | `ast.Constant`, value `node.value` |
| An untyped catch | `ast.ExceptHandler`, `node.type is None` |
| The line number | `node.lineno` |

Walking every node: `ast.walk(ast.parse(source))`. `ast.walk` does not go in
line order; if order matters the result is sorted by `lineno`.

## Keep in mind

- `ast.parse` does not run code; whatever the examined code is, the
  analysis is safe.
- Text search gives false alarms in comments and strings.
- An accepted false alarm is marked in the code with its reason.
