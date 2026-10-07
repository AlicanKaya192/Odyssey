Nesting can be two or three levels deep. Instead of writing each level by
hand, you will write a function that calls itself.

**What to do:**

1. Write the function `flatten(obj, prefix="")`. `obj` is a dictionary. In
   the flat dictionary it returns:
   - if a value is not a dictionary, it goes in as it is under the name
     `prefix + key`,
   - if a value is a dictionary, the function calls **itself** for it with
     the prefix `prefix + key + "_"` and adds the result (`update`).
   Lists stay as they are.
2. Flatten `record` and print every key and value as `name = value`.

**Expected output:**

```
id = 7
title = Emma
author_name = Austen
author_address_city = Bath
author_address_country = UK
tags = ['classic', 'novel']
```
