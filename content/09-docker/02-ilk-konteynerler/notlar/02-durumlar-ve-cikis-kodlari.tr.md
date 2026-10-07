`docker ps -a` çıktısındaki STATUS sütunu konteynerin hangi aşamada
olduğunu ve nasıl bittiğini söylüyor. Hata ayıklarken ilk bakılacak yer
burası.

## Durumlar

| Durum | Anlamı |
|---|---|
| **Created** | Oluşturuldu ama hiç çalıştırılmadı. |
| **Up 5 minutes** | Çalışıyor (5 dakikadır). |
| **Exited (0) 2 minutes ago** | Bitti; parantezdeki sayı çıkış kodu. |
| **Restarting** | Çöktü ve Docker yeniden başlatıyor (yeniden başlatma kuralı varsa). |
| **Paused** | `docker pause` ile donduruldu. |

## Çıkış kodu nedir?

Her program biterken işletim sistemine bir sayı bırakıyor: **çıkış kodu**.
`0` "her şey yolunda" demek; başka her sayı bir sorun. Python'da bir hata
yakalanmadan program biterse çıkış kodu `1` oluyor; `sys.exit(3)` yazarsan
`3`.

Konteynerin çıkış kodu, içindeki asıl programın çıkış kodu.

## Sık görülen kodlar

| Kod | Ne oldu? | Nereye bakmalı? |
|---|---|---|
| **0** | Program sorunsuz bitti. | — |
| **1** | Program bir hatayla bitti (Python'da yakalanmamış bir hata). | `docker logs ad` |
| **125** | Docker konteyneri hiç başlatamadı (yanlış seçenek, ad çakışması). | Komutun kendisi |
| **126** | Komut bulundu ama çalıştırılamadı (izin yok). | Dosya izinleri |
| **127** | Komut bulunamadı (yazım hatası ya da imajda yok). | Komutun adı |
| **137** | Program zorla öldürüldü (`docker kill`, bellek yetmedi ya da `stop` süresi doldu). | Bellek, `stop` |
| **143** | Program kapanma isteğini alıp düzgünce kapandı (`docker stop`). | — |

137 ve 143 sayıları rastgele değil: `128 + sinyal numarası`. 9 numaralı
sinyal "hemen öl" (SIGKILL), 15 numaralı "lütfen kapan" (SIGTERM).

## Kendin dene

```text
docker run --rm alpine:3.22 sh -c "exit 3"
echo $LASTEXITCODE
```

PowerShell'de son komutun çıkış kodu `$LASTEXITCODE` değişkeninde; çıktı
`3`. (`sh -c "..."` tırnak içindeki satırı kabukla çalıştırıyor.)

```text
docker run --rm alpine:3.22 olmayan-komut
```

Bu da 127'yle bitiyor; Docker hatanın sebebini de yazıyor (komut
bulunamadı).

## Ne zaman hangisi?

- Konteyner **hemen** bitiyorsa ve kod 0 değilse → `docker logs` ile
  programın son yazdığına bak.
- Kod 125–127 arasındaysa → sorun programda değil, **komutta**.
- Kod 137 ise → konteyner öldürüldü; bellek sınırı ya da `stop` süresi.
