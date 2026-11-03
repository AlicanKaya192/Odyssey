## Kavramlar

| Kavram | Anlamı |
|---|---|
| Yazılı izin | Sistemin sahibinin testi yazıyla onaylaması |
| Angajman kuralları | Testin kapsamını, zamanını ve sınırlarını söyleyen belge |
| Kapsam | İzin verilen adresler ve sistemler |
| Hariç tutulan | Kapsamın içinde olsa da test edilmeyen sistem |
| Zaman penceresi | Testin yapılabileceği günler ve saatler |
| Çift kullanımlı bilgi | Hem savunmada hem saldırıda kullanılabilen bilgi |
| Çıkar çatışması | Tarafsızlığı etkileyebilecek başka bir bağ |

## Teste başlamadan

- Yazılı izin var mı, izni veren o sistemin sahibi mi?
- Kapsam adres adres yazılı mı, hariç tutulanlar açık mı?
- Zaman penceresi ve saat dilimi belli mi?
- Acil durumda kim aranacak?
- Görülen veri nasıl saklanacak, ne zaman silinecek?
- Sistem bir bulut hizmetindeyse sağlayıcının test kuralları okundu mu?

## Python kalıpları

- Eksik alan: `[n for n in required if not plan.get(n)]`.
- Ağ içinde mi: `ipaddress.ip_address(a) in ipaddress.ip_network(cidr)`.
- Tarih aralığı: `start <= day <= end`.
- E-postayı maskelemek: `user[0] + "***@" + domain`.

## Akılda tutulacak

- İyi niyet izin yerine geçmez.
- İzin yazılı olana verilir; "nasılsa aynı ağ" kapsam değildir.
- Erişimi olmak, izin verebilmek demek değildir.
- Bir açığı göstermek için bütün veriyi indirmek gerekmez.
- Bu kart hukuki tavsiye değildir; ayrıntı için yasanın kendisine ve bir
  hukukçuya başvurulur.
