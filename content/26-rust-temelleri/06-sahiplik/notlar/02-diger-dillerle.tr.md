Başka bir dil biliyorsan fark şurada:

| Soru | Python | C | Rust |
|---|---|---|---|
| `b = a` sonra `a` | Kullanılabilir, aynı nesne | Kullanılabilir, aynı adres | **Kullanılamaz** (taşındı) |
| Bellek kim geri verir | Çöp toplayıcı | Programcı (`free`) | Derleyicinin eklediği kod |
| Geri vermeyi unutmak | Olmaz | Kolay | Çoğu durumda olmaz |
| Silinmişi okumak | Olmaz | Kolay, tehlikeli | **Derlenmez** |
| Çalışırken ek yük | Var | Yok | Yok |

## Python gözüyle

Python'da `b = a` aynı listeye iki ad verir. Birini değiştirince öteki de değişir ve bu sık bir hata kaynağıdır. Rust'ta bu durum baştan yoktur: Bir anda
tek sahip vardır.

## C gözüyle

C'de `free` çağrısını sen yazarsın. Rust'ta kapsam sonu aynı işi görür ve yanlış yazman mümkün değildir. Bu fikrin C++'taki adı RAII'dir: kaynak, nesnenin
ömrüne bağlanır.

## Bu yalnızca bellek için değil

Kapsam sonu temizliği her kaynak için çalışır: Dosya değişkeni kapsamdan çıkınca dosya kapanır, kilit değişkeni çıkınca kilit bırakılır. Unutma ihtimali kalmaz.

## Rust yine de bellek kaçırabilir mi?

Kaçırabilir. Bellek kaçırmak Rust'ın güvenlik garantisinin dışındadır. `Box::leak` ya da birbirini gösteren `Rc` döngüleri belleği geri vermez, ama bunlar bilerek
yazılır. İkinci modülde `Rc`'yi görürken bunu ölçeceğiz.
