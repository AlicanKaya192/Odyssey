İki değişiklik yap:

- `test` işine bir `env:` bölümü ekle: `APP_ENV` değişkeni `test` değerini alsın. Yorumun yerine, `runs-on` ile aynı hizada.
- İki kurulum adımını (`--upgrade pip` ve `requirements.txt`) **tek bir adımda** birleştir: `run: |` ile iki satır. Bu adımın adı `Install dependencies` olsun.
