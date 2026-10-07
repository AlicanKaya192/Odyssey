**Yapman gereken:** bütün alanları isteğe bağlı bir `Settings` modeli ve onu
olduğu gibi döndüren `POST /settings`.

| Alan | Tip | Varsayılan |
|---|---|---|
| `theme` | metin | `"dark"` |
| `font_size` | tam sayı | `14` |
| `beta` | bool | `False` |

- `{}` → `{"theme": "dark", "font_size": 14, "beta": false}`
- `{"font_size": 18}` → `{"theme": "dark", "font_size": 18, "beta": false}`
- `{"font_size": "big"}` → `422`
