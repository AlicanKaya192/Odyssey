**What to do:** a `Settings` model whose fields are all optional, and
`POST /settings` that returns it as it is.

| Field | Type | Default |
|---|---|---|
| `theme` | string | `"dark"` |
| `font_size` | integer | `14` |
| `beta` | bool | `False` |

- `{}` → `{"theme": "dark", "font_size": 14, "beta": false}`
- `{"font_size": 18}` → `{"theme": "dark", "font_size": 18, "beta": false}`
- `{"font_size": "big"}` → `422`
