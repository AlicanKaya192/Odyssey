`ll` yazınca `ls -l` çalışsın ve bu, her yeni terminalde de geçerli olsun.

- `~/.bashrc` dosyasının **sonuna** şu satırı ekle (dosyadaki öteki satırlar silinmesin):

```text
alias ll='ls -l'
```

- Dosyayı şu anki terminale okut ve `ll names.txt` ile dene.
