Bu iş akışı çalışıyor ama adımların adı yok; kayıtlarda hangisinin düştüğünü bulmak zor.

Her adıma, `uses`/`run` satırının üstüne aynı hizada bir `name:` ekle. Adlar tam olarak şunlar olsun:

- `Get the code`
- `Set up Python`
- `Install dependencies`
- `Run tests`

Adım `- name: ...` ile başlar, `uses:` ya da `run:` bir alt satırda, `name`'le aynı hizada devam eder.
