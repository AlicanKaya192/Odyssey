**Yükleme ve indirme**

| Eylem | Ayar | Anlamı |
|---|---|---|
| `actions/upload-artifact@v4` | `name` | Artifact'in adı (çalışmada eşsiz) |
| | `path` | Yüklenecek dosya ya da klasör |
| | `retention-days` | Kaç gün saklanacak (varsayılan 90) |
| `actions/download-artifact@v4` | `name` | Hangi artifact; yazılmazsa hepsi |
| | `path` | İndirilecek klasör |

**Önbellek mi artifact mi?**

| | Önbellek | Artifact |
|---|---|---|
| Amaç | Hız | Ürün |
| Bulunur | Anahtarla | Adla |
| Ait olduğu | Dal | Çalışma |
| Elle indirilir | Hayır | Evet, çalışma sayfasından |
| Kaybolursa | İş yine çalışmalı | Ürün yok |

**Sık kalıplar**

```yaml
      # Derleme işi
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

      # Sonraki iş (needs: build)
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: pip install dist/*.whl
```

```yaml
      # Testler düşse de rapor
      - run: python -m pytest --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: report-${{ matrix.os }}
          path: report.xml
          retention-days: 14
```

**Kurallar**

- Bir kez derle; test edilen ve yayınlanan aynı dosya.
- Duman testi işinde `checkout` yok: yalnızca paket.
- Matriste ad matristen: aynı adla iki yükleme olmaz.
- Rapor `if: always()`: en çok düştüğünde gerekir.
