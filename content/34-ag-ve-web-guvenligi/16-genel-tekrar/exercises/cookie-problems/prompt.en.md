Apply the Sessions and Cookies section. `cookie_problems(header)`
should split a `Set-Cookie` value at `;`. The **first part** is the
cookie's name and value and does not count as an attribute. Looking at the
names of the remaining parts (before `=`, `strip`, lower case), return
those missing from `Secure`, `HttpOnly`, `SameSite` **in this order**.

**Expected output:**

```
[]
['Secure', 'SameSite']
['Secure', 'HttpOnly', 'SameSite']
[]
```
