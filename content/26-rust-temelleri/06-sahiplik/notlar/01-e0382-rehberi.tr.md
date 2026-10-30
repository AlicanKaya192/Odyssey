`E0382` gördüğünde dört çıkış yolu var. Sırayla düşün.

## 1. Taşımaya gerek var mı?

Çoğu zaman fonksiyonun değere sahip olması gerekmez, yalnızca okuması yeter. Çözüm ödünç almak (`&name`), sonraki bölümün konusu.

## 2. Sırayı değiştirebilir misin?

Değeri son kullanımdan sonra taşı:

```rust
fn take(text: String) {
    println!("took {text}");
}

fn main() {
    let name = String::from("Ada");
    println!("{name}");
    take(name);
}
```

```text
Ada
took Ada
```

## 3. Gerçekten iki bağımsız kopya mı lazım?

`.clone()` yaz. Bedeli görünür olduğu için ayıp değildir; ama döngü içindeki `.clone()`'a bir daha bak.

## 4. Döngüde mi taşındı?

Klasik bir tuzak. İlk turda taşınan değer ikinci turda yoktur:

```rust
fn take(text: String) {
    println!("{text}");
}

fn main() {
    let name = String::from("Ada");
    for _ in 0..2 {
        take(name);
    }
}
```

```text
error[E0382]: use of moved value: `name`
 --> main.rs:8:14
  |
6 |     let name = String::from("Ada");
  |         ---- move occurs because `name` has type `String`, which does not implement
  the `Copy` trait
7 |     for _ in 0..2 {
  |     ------------- inside of this loop
8 |         take(name);
  |              ^^^^ value moved here, in previous iteration of loop
  |
note: consider changing this parameter type in function `take` to borrow instead if
owning the value isn't necessary
 --> main.rs:1:15
  |
1 | fn take(text: String) {
  |    ----       ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
help: consider cloning the value if the performance cost is acceptable
  |
8 |         take(name.clone());
  |                  ++++++++
```

Mesaj `value moved here, in previous iteration of loop` diyor. Çözüm yine `.clone()` ya da ödünç almak.

## Kısmi taşıma

Demetin ya da yapının bir parçası taşınırsa o parça kullanılamaz, öteki parçalar kullanılabilir:

```rust
fn main() {
    let pair = (String::from("key"), 7);
    let key = pair.0;
    println!("{key} {}", pair.1);
}
```

```text
key 7
```

`pair.0` taşındı ama `pair.1` bir sayı ve `Copy`. Artık `pair`'in bütünü kullanılamaz, `pair.1` kullanılabilir.

## Hata mesajını okumak

| Mesaj parçası | Ne demek |
|---|---|
| `move occurs because ... does not implement the Copy trait` | Bu tür kopyalanmıyor, taşınıyor |
| `value moved here` | Sahipliğin gittiği satır |
| `value used here after move` | Sonraki kullanım |
| `consider cloning` | Hızlı çözüm önerisi; en iyisi olmayabilir |
