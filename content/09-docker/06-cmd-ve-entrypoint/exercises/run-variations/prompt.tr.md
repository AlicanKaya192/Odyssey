**Yapman gerekenler:** `commands.sh` dosyasına sırayla dört komut yaz:

1. `greet` imajını `Ada` argümanıyla çalıştır; bitince silinsin.
2. `greet` imajının içine `sh` ile gir: `ENTRYPOINT`'i bir kerelik değiştir,
   klavye ve terminal ver, bitince silinsin.
3. `worker` imajını sinyalleri ileten başlatıcıyla (`--init`), arka planda,
   `worker` adıyla çalıştır.
4. `worker` konteynerini durdur; kapanması için **30 saniye** ver.
