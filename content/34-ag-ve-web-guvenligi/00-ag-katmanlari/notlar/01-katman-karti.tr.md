## TCP/IP katmanları

| Katman | OSI no | Ne taşır? | Örnek |
|---|---|---|---|
| Uygulama | 7 | Programın mesajı | HTTP, DNS, SSH |
| Taşıma | 4 | Port numaraları | TCP, UDP |
| Ağ | 3 | IP adresleri | IPv4, IPv6 |
| Bağlantı | 2 | MAC adresleri | Ethernet, Wi-Fi |

Kapsülleme: veri → segment (TCP başlığı) → paket (IP başlığı) → çerçeve
(Ethernet başlığı). Alıcı ters sırayla söker.

## Adres aralıkları

| Aralık | Anlamı |
|---|---|
| `10.0.0.0/8` | Özel |
| `172.16.0.0/12` | Özel (`172.16` – `172.31`) |
| `192.168.0.0/16` | Özel |
| `127.0.0.0/8` | Geri döngü (bu bilgisayar) |
| `169.254.0.0/16` | Bağlantı yerel (adres alınamadığında) |
| `203.0.113.0/24` | Belgelerde örnek için ayrılmış |

## Bilinen portlar

| Port | Servis | Port | Servis |
|---|---|---|---|
| 22 | SSH | 443 | HTTPS |
| 25 | SMTP | 3306 | MySQL |
| 53 | DNS | 5432 | PostgreSQL |
| 80 | HTTP | 3389 | Uzak masaüstü |

## Python kalıpları

- Adres: `ipaddress.ip_address("192.168.1.10")`; `int(ip)`, `ip.version`.
- Ağ: `ipaddress.ip_network("192.168.1.0/24")`; `net.num_addresses`,
  `net.netmask`, `net.broadcast_address`.
- İçinde mi: `ip in net`.
- Tür: `ip.is_loopback`, `ip.is_private`, `ip.is_global`. Geri döngü de
  `is_private` sayılır: önce `is_loopback`'e bak.
- Alt ağlara böl: `net.subnets(new_prefix=26)`.

## TCP ve UDP

| | TCP | UDP |
|---|---|---|
| Bağlantı | Var (SYN, SYN-ACK, ACK) | Yok |
| Kayıp | Yeniden gönderilir | Kaybolur |
| Sıra | Korunur | Garanti yok |
| Örnek | HTTP, SSH, e-posta | DNS sorgusu, görüntülü görüşme |
