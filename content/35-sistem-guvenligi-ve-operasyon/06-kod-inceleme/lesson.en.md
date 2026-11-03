# Code Review and Static Analysis

In the Secure Software Development section we saw that one of the security
jobs of the coding step is **code review**. Before a change goes into the
main code, at least one more person reads it. Review catches bugs early,
spreads knowledge across the team, and leaves nothing that "nobody saw".

The human eye gets tired and is not suited to searching for the same thing
a thousand times. That is why **static analysis** is used alongside
review: tools that look for bugs by reading the code's text or structure,
**without running it**. This section covers both together and builds a
small static analysis tool with Python's `ast` module. The code being
examined is only text; none of it is run.

## What does a reviewer look at?

| Question | Example |
|---|---|
| Where does the input come from, is it validated? | Does a number from a form pass a range check? |
| Is there an authorization check, in the right place? | Does every endpoint check ownership? |
| What happens on an error? | Does the check refuse when there is an error? |
| Is a secret in the code? | Is a password or key written into a file? |
| Is there a dangerous function? | `eval`, `exec`, unsafe deserialisation |
| What was **removed**? | Does the change remove a check? |

The last question is the easiest to skip: the reviewer focuses on the
added lines, yet a security check being silently removed is the most
dangerous change.

## Searching text is not enough

The simplest static analysis is searching text. Let us find the lines
containing `eval(`:

```python
SOURCE = '''# never call eval( on user input
note = "eval( is dangerous"
total = eval(expression)
'''
hits = [n for n, line in enumerate(SOURCE.splitlines(), 1) if "eval(" in line]
print(hits)
```

```text
[1, 2, 3]
```

All three lines were caught, but only the third is a real call: the first
is a comment, the second a string. These are called **false positives**. A
tool that gives many false alarms is ignored after a while; that means
real findings get missed.

## Looking at structure: the syntax tree

Before Python code runs it is turned into an **abstract syntax tree**
(AST). The `ast` module gives this tree to us too. The tree has no
comments, strings stay strings, and a function call is a `Call` node. Let
us scan the same source with the tree:

```python
import ast

DANGEROUS = {"eval", "exec"}
for node in ast.walk(ast.parse(SOURCE)):
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") in DANGEROUS:
        print(node.lineno, node.func.id)
```

```text
3 eval
```

Only the real call was found. `ast.parse` does **not run** the code, it only
extracts its structure; so however dangerous the examined code is, the
analysis is safe. Real static analysis tools apply the same idea with much
larger rule lists.

## Secrets in the code

A password written into source code is open to everyone who can see the
code: in the repository history, in backups, in copies. Let us look for a
**fixed string** being assigned to a variable whose name contains
`password`, `secret` or `token`:

```python
import ast

CODE = '''
db_password = "hunter2"
api_token = load_from_vault("api")
retries = 3
SECRET_KEY = "dev-key-123"
'''
WORDS = ("password", "secret", "token")
for node in ast.walk(ast.parse(CODE)):
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
        if not isinstance(node.value.value, str):
            continue
        for target in node.targets:
            name = getattr(target, "id", "")
            if any(word in name.lower() for word in WORDS):
                print(node.lineno, name)
```

```text
2 db_password
5 SECRET_KEY
```

`db_password` and `SECRET_KEY` were caught because they are assigned fixed
strings. `api_token` was counted as clean because it comes from a function
(a secrets vault); that is the right way too (the Secrets Management
section). `retries` is a number and its name is not suspicious.

## Silently swallowing errors

`except:` (a catch with no type written) catches every error. If it sits
around a security check, the check's error is silently swallowed and the
code carries on; this is exactly the failing open from the Secure Software
Development section:

```python
import ast

CODE = '''
try:
    check_permission(user)
except:
    pass
delete_everything()
'''
for node in ast.walk(ast.parse(CODE)):
    if isinstance(node, ast.ExceptHandler) and node.type is None:
        print("bare except at line", node.lineno)
```

```text
bare except at line 4
```

If the permission check raises an error, `pass` swallows it and the next
line runs anyway. In the tree, a catch with no type is an `ExceptHandler`
whose `type` field is `None`; finding it is that easy.

## Looking at the diff: what was removed?

A review usually reads not the whole file but the change's **diff**. In a
diff, lines starting with `+` are added and lines starting with `-` are
removed:

```python
DIFF = """--- a/app.py
+++ b/app.py
@@ -10,3 +10,4 @@
 def save(user, data):
-    check_owner(user, data)
+    log(user)
     store(data)
+    return True
"""
lines = DIFF.splitlines()
removed = [l[1:].strip() for l in lines if l.startswith("-") and not l.startswith("---")]
added = [l[1:].strip() for l in lines if l.startswith("+") and not l.startswith("+++")]
print("removed:", removed)
print("added:", added)
```

```text
removed: ['check_owner(user, data)']
added: ['log(user)', 'return True']
```

The two added lines look harmless. What matters is the removed line: the
ownership check was taken out. If this change is approved, the door opens
to horizontal privilege escalation (the Privilege Escalation section). A
reviewer looks at the removed lines first.

## Tool and human

<figure class="fig"><div class="versus">
  <div><h4>Static analysis tool</h4>Never tires, applies the same rules on every change, quickly finds known patterns (a dangerous function, a secret in the code). But it does not know the <b>intent</b> and gives false alarms.</div>
  <div><h4>Human reviewer</h4>Understands what the code is trying to do, sees a missing check or a logic bug. But gets tired and cannot search for the same thing a thousand times.</div>
</div><figcaption>Neither replaces the other; the tool checks patterns, the human checks meaning.</figcaption></figure>

Tools are put in the build pipeline (CI) and run automatically on every
change. If a finding is to be accepted deliberately (it really is a false
alarm), this is marked in the code with its reason; it is not silently
ignored.

## Summary

- **Code review:** someone else reads a change before it goes into the main
  code; input, authorization, error handling, secrets and **removed
  lines** are questioned.
- **Static analysis:** looks for bugs by reading code without running it.
- Searching text also catches comments and strings: **false positives**.
- The **AST** gives the code's structure; `ast.parse` does not run the
  code.
- Secrets assigned as fixed strings, untyped `except:` and dangerous calls
  are easy to find with the tree.
- The tool checks patterns, the human checks meaning; both are used
  together.
