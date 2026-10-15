**İzinler: en az yetki**

```yaml
permissions:
  contents: read

jobs:
  release:
    permissions:
      contents: write
```

- Üstteki blok bütün işlerin varsayılanı; işteki blok onu ezer.
- `permissions:` yazılınca listede olmayan her izin `none` olur.

| İzin | Ne için | Çoğu iş |
|---|---|---|
| `contents` | Dosyalar, etiketler, sürümler | `read`; sürüm açan iş `write` |
| `pull-requests` | PR'a yorum, etiket | Gerekirse `write` |
| `packages` | Paket ve imaj deposu | Yükleyen iş `write` |
| `id-token` | Buluta şifresiz giriş | Dağıtan iş `write` |

**Eylemleri sabitlemek**

| Yazım | Değişebilir mi? |
|---|---|
| `actions/checkout@v4` | Evet; etiket başka commit'e taşınabilir |
| `actions/checkout@main` | Her gün; dal ilerler |
| `actions/checkout@` + 40 karakterlik commit kimliği | Hayır |

Commit kimliğiyle sabitlerken satır sonuna sürümü yorum olarak yaz
(`# v4`); güncellemeyi elle ya da Dependabot ile yap.

**Kod enjeksiyonu**

Dışarıdan gelen değerler: PR başlığı ve gövdesi, dal adı, commit mesajı,
yorum metni, issue başlığı. Bunlar `run:`'a doğrudan yazılmaz.

```yaml
      # Tehlikeli: başlık komutun parçası olur
      - run: echo "PR title is ${{ github.event.pull_request.title }}"
```

```yaml
      # Güvenli: başlık bir değişkenin değeri olur
      - run: echo "PR title is $TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

**`pull_request_target` dikkat**

`pull_request` fork'tan gelen PR'a gizli değer vermez. `pull_request_target`
ise iş akışını hedef dalın sürümüyle, gizli değerler ve yazma izniyle
çalıştırır. Bu tetikleyicide PR'ın kodunu çekip çalıştırmak, gizli
değerleri PR'ı açan kişiye vermek demektir. Gerekmedikçe kullanma.

**Kontrol listesi**

- Kodda anahtar yok; hepsi kasada.
- Gizli değer `env:` ile yalnızca isteyen adımda.
- Üstte `permissions: contents: read`.
- Gizli değer isteyen işler PR'da çalışmıyor.
- Dışarıdan gelen metin `env:` üzerinden.
- Güvenilir eylemler; kritik hatta commit kimliğiyle sabit.
