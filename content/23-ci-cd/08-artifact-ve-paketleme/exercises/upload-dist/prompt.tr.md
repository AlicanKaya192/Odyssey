`build` işi paketi derliyor ama dosyalar makineyle birlikte kayboluyor. Derlemeden sonra bir `actions/upload-artifact@v4` adımı ekle:

- Artifact'in adı `dist`
- Yüklenecek klasör `dist/`
