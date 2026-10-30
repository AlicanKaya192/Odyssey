## Komut bulunamıyor

`rustc : The term 'rustc' is not recognized` gibi bir mesaj, kurulumun bittiğini ama
terminalin bunu henüz bilmediğini gösterir. Rust'ın klasörü `%USERPROFILE%\.cargo\bin`
adresindedir ve yalnızca kurulumdan **sonra** açılan programlar onu görür.

1. Terminali kapatıp yeniden aç. Odyssey için de aynısını yap.
2. Yine olmuyorsa bilgisayarı yeniden başlat.
3. Hâlâ yoksa kurulum yarım kalmıştır: `rustup-init.exe` dosyasını yeniden çalıştır.

## Bağlayıcı bulunamadı

`linker link.exe not found` mesajı, derleyicinin kurulu olduğunu ama programı birleştirecek
parçanın eksik olduğunu söyler. Bu parça Visual Studio ile geliyor; kurulumda bu adım atlanmış
olabilir. `rustup-init.exe` dosyasını yeniden çalıştırıp Visual Studio adımını kabul et. Ayrıntılı
yönerge: `https://rust-lang.github.io/rustup/installation/windows-msvc.html`.

## Program derleniyor ama Windows engelliyor

Windows 11'de Akıllı Uygulama Denetimi (Smart App Control) açıksa bilgisayarında yeni üretilmiş,
imzasız programları engelleyebilir. Odyssey bu durumda "Windows derlenen programı engelledi" der.
Kodun yanlış değildir. Bu ayar bilgisayarının güvenlik ayarıdır ve kararı sana aittir.

## Faydalı rustup komutları

| Komut | Ne yapar |
|---|---|
| `rustup update` | Rust'ı son sürüme yükseltir |
| `rustup show` | Hangi sürümün kullanıldığını gösterir |
| `rustup doc` | Yerel belgeleri tarayıcıda açar, internet istemez |
| `rustup self uninstall` | Rust'ı bilgisayardan kaldırır |

`rustup doc` özellikle değerlidir: Resmî kitap (*The Rust Programming Language*) ve standart
kütüphanenin bütün belgeleri kurulumla birlikte bilgisayarına gelir.

## Editör

Odyssey'deki alıştırmalar için ayrıca editör gerekmez. Kendi projelerinde VS Code ve
`rust-analyzer` eklentisi yaygın bir seçimdir: Hataları yazarken gösterir, türleri satırın
üstünde yazar.
