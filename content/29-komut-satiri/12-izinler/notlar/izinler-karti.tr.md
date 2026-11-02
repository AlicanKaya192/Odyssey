İzinlerin hepsi, bir bakışta.

## Okumak

```text
-rwxr-xr--
│└┬┘└┬┘└┬┘
│ │  │  └ diğerleri (o)
│ │  └─── grup (g)
│ └────── sahip (u)
└──────── tür: - dosya, d klasör
```

## Harfler

| İzin | Dosyada | Klasörde |
|---|---|---|
| `r` | İçini okumak | İçindekileri listelemek |
| `w` | İçini değiştirmek | İçinde dosya açmak, silmek, adını değiştirmek |
| `x` | Program gibi çalıştırmak | İçine girmek, içindekilere ulaşmak |

## Sayılar

| Rakam | İzin | Rakam | İzin |
|---|---|---|---|
| 7 | `rwx` | 3 | `-wx` |
| 6 | `rw-` | 2 | `-w-` |
| 5 | `r-x` | 1 | `--x` |
| 4 | `r--` | 0 | `---` |

| Sayı | Görünüm | Ne zaman |
|---|---|---|
| 644 | `rw-r--r--` | Sıradan dosya |
| 600 | `rw-------` | Gizli dosya (anahtar, şifre dosyası) |
| 755 | `rwxr-xr-x` | Betik, program, klasör |
| 700 | `rwx------` | Yalnızca senin klasörün |
| 444 | `r--r--r--` | Salt okunur |

## chmod

| Yazım | Ne yapar |
|---|---|
| `chmod +x f` | Herkese çalıştırma ekler |
| `chmod u+x f` | Yalnızca sahibe çalıştırma ekler |
| `chmod go-rwx f` | Grup ve diğerlerinin her iznini kaldırır |
| `chmod a=r f` | Herkese tam olarak yalnızca okuma |
| `chmod g+w,o-r f` | İki değişiklik birden |
| `chmod 600 f` | Sayıyla, hepsini baştan yazar |

## Hatırla

- `./betik` için `x` gerekir; `bash betik` için `r` yeter.
- Dosyaya giden yoldaki her klasörde `x` gerekir.
- `chmod 777` kolay ama güvensiz; en az izni ver.
