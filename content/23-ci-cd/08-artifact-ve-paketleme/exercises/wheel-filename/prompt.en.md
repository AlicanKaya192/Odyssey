Write the function `wheel_filename(name, version)`. It should return the wheel file name of a pure Python package:

- The form: `name-version-py3-none-any.whl`
- The name is first turned into lowercase.
- The `-`, `_` and `.` characters in the name become `_`; consecutive ones become a **single** `_` (`a__b--c` → `a_b_c`).

`"My-Package"`, `"1.0"` → `"my_package-1.0-py3-none-any.whl"`

**Expected output:**

```
greeter-0.1.0-py3-none-any.whl
my_package-1.0-py3-none-any.whl
data_tools-2.3.1-py3-none-any.whl
a_b_c-0.0.1-py3-none-any.whl
```
