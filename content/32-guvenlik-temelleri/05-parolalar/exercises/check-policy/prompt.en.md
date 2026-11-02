`check_policy(password, username, common)` should check a password
against today's guidelines and return the list of problems in this order:

1. `"too-short"`: if it is shorter than 12 characters,
2. `"common"`: if it is in the `common` list, ignoring upper and lower
   case,
3. `"has-username"`: if the username is not empty and appears inside the
   password, ignoring upper and lower case.

An empty list if there are no problems. There is **no** character type
rule.

**Expected output:**

```
['too-short', 'common']
['has-username']
[]
```
