Her servis bir Dockerfile istemiyor; hazır bir imaj da kullanılabilir.

**Yapman gereken:** `worker` adında bir servis:

1. Hazır `alpine:3.22` imajını kullansın (`image`).
2. Komutu `sh -c "echo hello from compose && sleep 300"` olsun (`command`,
   köşeli parantezli biçimde üç parça).

Odyssey servisi ayağa kaldıracak, çalıştığına ve günlüğünde
`hello from compose` yazdığına bakacak.
