`module_kind(name)` fonksiyonunu yaz ve sırayla bak:
`sys.builtin_module_names` içindeyse `"built-in"`, `sys.stdlib_module_names`
içindeyse `"standard"`, `importlib.util.find_spec(name)` bir şey buluyorsa
`"third-party"`, hiçbiri değilse `"missing"` döndürsün.

**Beklenen çıktı:**

```
math built-in
json standard
numpy third-party
no_such_module_x missing
```
