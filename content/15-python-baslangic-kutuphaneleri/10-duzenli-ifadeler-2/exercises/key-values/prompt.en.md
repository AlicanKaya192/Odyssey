Write the function `key_values(text)`: turn `key=value` pairs separated
by `;`, like `"name=Ada; age=36"`, into a dictionary. There may be spaces
around `=`; strip the spaces at the start and end of each value. The
pattern: `(\w+)\s*=\s*([^;]+)`; `findall` gives the groups.

**Expected output:**

```
name Ada
age 36
city London
{'mode': 'test', 'debug': '1'}
```
