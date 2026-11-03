Dosya yükleme, girdi doğrulamanın en çok katmanlı olduğu yerdir: dosyanın
adı, türü, boyutu ve içeriği ayrı ayrı girdidir.

## Ad

- Kullanıcının verdiği adı diskte dosya adı olarak **kullanma**. Dosyayı
  rastgele bir adla sakla (`secrets.token_hex(16)`), asıl adı
  veritabanında etiket olarak tut.
- Ad gösterilecekse ekrana yazarken kodla (XSS).
- Ad bir yola eklenecekse normalleştir ve klasörün içinde mi denetle (yol
  geçişi).

## Tür

- Uzantıya (`.png`) ve tarayıcının bildirdiği türe güvenme; ikisi de
  kullanıcının elindedir.
- İzin verilen türleri bir **listeyle** sınırla (yalnızca resim gibi) ve
  dosyanın ilk baytlarına bakarak gerçekten o tür mü denetle.
- Sunucunun yüklenen dosyayı **çalıştırabileceği** bir yere koyma
  (betik olarak yorumlanabilen klasörler).

## Boyut

- En büyük boyutu sınırla ve okurken sınırı aşınca dur; bütün dosyayı
  belleğe alıp sonra ölçme.
- Sıkıştırılmış dosyalarda açılmış boyut da sınırlanır: küçük bir arşiv
  çok büyük bir içeriğe açılabilir.

## İçerik

- Resimler yeniden işlenerek (yeniden kodlanarak) saklanabilir; içine
  gizlenmiş fazladan veri atılır.
- Dosyalar ayrı bir alan adından sunulursa, içlerinde bir şey çalışsa bile
  ana sitenin çerezlerine ve sayfalarına ulaşamaz.

## Kısa kontrol listesi

- [ ] Rastgele dosya adı, asıl ad yalnızca etiket.
- [ ] Tür izin listesi + ilk baytlarla denetim.
- [ ] Boyut sınırı (sıkıştırılmışta açılmış boyut da).
- [ ] Çalıştırılamayan bir yerde saklama.
- [ ] Mümkünse ayrı bir alan adından sunma.
