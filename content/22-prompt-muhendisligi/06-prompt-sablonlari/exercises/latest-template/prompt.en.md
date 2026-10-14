`render_latest(templates, name, values)` should pick the largest version
**as a number** among the versions in `templates[name]` (the keys are
texts such as `"1"`, `"2"`, `"10"`) and fill it with
`str.format(**values)`. Return `[version number (int), text]`. If the
template name does not exist, `[0, ""]`.

**Expected output:**

```
10
Pick one category: Hi
[0, '']
```
