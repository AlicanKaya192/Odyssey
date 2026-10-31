# Performans

Rust hızlıdır, ama hızlı program kendiliğinden çıkmaz. Bu bölümde üç şey var: Doğru ölçmek, gereksiz işi kaldırmak ve bellek düzenini işlemciye uygun yapmak.

Bölümdeki süreler **bu bilgisayarda** ölçüldü, sende farklı çıkar. Önemli olan sayılar değil, aralarındaki oran. Alıştırmalar da süreye bakmıyor: Ayırma sayıyor, boyut ölçüyor; bu sayılar her makinede aynı.

## Önce doğru ölçmek

Debug derlemesi eniyileme yapmaz, çünkü amacı hızlı derlemek ve hata ayıklamaktır. Aynı kod iki profilde:

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..50_000_000u64 {
        total = total.wrapping_add(black_box(i));
    }
    println!("total {total}");
    println!("time: {} ms", start.elapsed().as_millis());
}
```

```text
$ cargo run
total 1249999975000000
time: 384 ms
```

```text
$ cargo run --release
total 1249999975000000
time: 20 ms
```

Yavaş bulduğun programa bakmadan önce `--release` ile çalıştırdığından emin ol. Debug'da yapılan ölçüm hiçbir şey söylemez.

İkinci tuzak ters yönde. Derleyici sonucu kullanılmayan işi siler:

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..500_000_000u64 {
        total = total.wrapping_add(i);
    }
    println!("unused: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let mut total = 0u64;
    for i in 0..500_000_000u64 {
        total = total.wrapping_add(black_box(i));
    }
    println!("{total}");
    println!("measured: {} ms", start.elapsed().as_millis());
}
```

```text
unused: 0 ms
124999999750000000
measured: 185 ms
```

İlk döngü ölçülmedi, çünkü yok: Derleyici onu kaldırdı. `black_box`, "bu değeri bilmiyormuş gibi davran" der ve işin silinmesini önler. Ölçüm kodunda sonucu `black_box`'tan geçir.

Üçüncü kural: Zaman nereye gidiyorsa oraya bak. Program zamanının büyük kısmını genelde küçük bir bölgede geçirir (**sıcak bölge**). Ölçmeden yapılan iyileştirme çoğunlukla zamanın hiç gitmediği yeri düzeltir.

## Ayırmalar

Bellek ayırmak görece pahalıdır ve sayılabilir. Geçen bölümdeki sayan ayırıcıyı kullanıyoruz; artık `realloc`'u da sayıyor:

```rust
fn main() {
    println!("push: {}", count_of(|| {
        let mut values = Vec::new();
        for i in 0..1000u32 {
            values.push(i);
        }
        black_box(values);
    }));
    println!("with_capacity: {}", count_of(|| {
        let mut values = Vec::with_capacity(1000);
        for i in 0..1000u32 {
            values.push(i);
        }
        black_box(values);
    }));
}
```

```text
push: 9
with_capacity: 1
```

`Vec` dolunca daha büyük yer alıp taşınır. Boyutu biliyorsan `with_capacity` tek ayırmaya indirir.

Döngüdeki `format!` her turda yeni `String` üretir. Bir tamponu temizleyip yeniden kullanmak aynı işi yapar:

```rust
use std::fmt::Write;

fn main() {
    println!("format!: {}", count_of(|| {
        for i in 0..1000 {
            black_box(format!("line {i}"));
        }
    }));
    println!("one buffer: {}", count_of(|| {
        let mut buffer = String::with_capacity(32);
        for i in 0..1000 {
            buffer.clear();
            write!(buffer, "line {i}").unwrap();
            black_box(&buffer);
        }
    }));
}
```

```text
format!: 1000
one buffer: 1
```

`clear` kapasiteyi korur, belleği bırakmaz. En ucuz ayırma, hiç yapılmayandır:

```rust
fn main() {
    let words = vec![String::from("one"), String::from("two"), String::from("three")];
    println!("clone: {}", count_of(|| {
        let mut total = 0;
        for word in &words {
            let copy = word.clone();
            total += copy.len();
        }
        black_box(total);
    }));
    println!("borrow: {}", count_of(|| {
        let mut total = 0;
        for word in &words {
            total += word.len();
        }
        black_box(total);
    }));
}
```

```text
clone: 3
borrow: 0
```

Iterator, dilim ve `&str` çoğu kopyayı gereksiz kılar. Kopyanın yalnızca bazen gerektiği yerde `Cow` kullanılır: Değişmiyorsa ödünç verir, değişiyorsa kopyalar.

## Boyut

Yapı ne kadar küçükse belleğe o kadar çok sığar:

```rust
struct Mixed {
    a: u8,
    b: u32,
    c: u8,
}

#[repr(C)]
struct MixedC {
    a: u8,
    b: u32,
    c: u8,
}

enum Heavy {
    Ping,
    Blob([u8; 256]),
}

enum Light {
    Ping,
    Blob(Box<[u8; 256]>),
}

fn main() {
    println!("Mixed {}", size_of::<Mixed>());
    println!("MixedC {}", size_of::<MixedC>());
    println!("Option<u32> {}", size_of::<Option<u32>>());
    println!("Option<Box<u8>> {}", size_of::<Option<Box<u8>>>());
    println!("String {}", size_of::<String>());
    println!("Heavy {}", size_of::<Heavy>());
    println!("Light {}", size_of::<Light>());
    let _ = (Heavy::Ping, Light::Ping, Heavy::Blob([0; 256]));
    let _ = Light::Blob(Box::new([0; 256]));
    let m = Mixed { a: 1, b: 2, c: 3 };
    let n = MixedC { a: 1, b: 2, c: 3 };
    let _ = (m.a, m.b, m.c, n.a, n.b, n.c);
}
```

```text
Mixed 8
MixedC 12
Option<u32> 8
Option<Box<u8>> 8
String 24
Heavy 257
Light 8
```

Her satırın bir dersi var:

- `Mixed` 8, `MixedC` 12: Rust alanları boşluk azaltacak şekilde yeniden dizer, `repr(C)` yazıldığı sırayı korur.
- `Option<u32>` 8: `None`'u göstermek için ayrı alan gerekti.
- `Option<Box<u8>>` 8: `Box` hiç boş olamaz, Rust boş işaretçiyi `None` için kullanır.
- `Heavy` 257: Her değer en büyük varyant kadar yer kaplar, `Ping` bile.
- `Light` 8: Büyük varyantı `Box`'a alınca yalnızca işaretçi kalır.

## Önbellek: Bellek sırası hızdır

İşlemci belleği küçük parçalar hâlinde okuyup yakınındaki önbellekte tutar. Yani yan yana duran veriyi okumak, uzağa atlamaktan çok daha ucuzdur. Aynı toplama, aynı sayıda işlem:

```rust
use std::hint::black_box;
use std::time::Instant;

const SIZE: usize = 4000;

fn main() {
    let grid = vec![1u32; SIZE * SIZE];

    let start = Instant::now();
    let mut sum = 0u32;
    for row in 0..SIZE {
        for column in 0..SIZE {
            sum = sum.wrapping_add(black_box(grid[row * SIZE + column]));
        }
    }
    black_box(sum);
    println!("rows: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let mut sum = 0u32;
    for column in 0..SIZE {
        for row in 0..SIZE {
            sum = sum.wrapping_add(black_box(grid[row * SIZE + column]));
        }
    }
    black_box(sum);
    println!("columns: {} ms", start.elapsed().as_millis());
}
```

```text
rows: 7 ms
columns: 104 ms
```

Tablo bellekte satır satır durur. Satır satır gezmek hep komşuya gider; sütun sütun gezmek her adımda 4000 eleman atlar.

Kodda her okumayı `black_box`'tan geçirdik. Geçirmezsek şu çıkıyor:

```text
rows: 3 ms
columns: 3 ms
```

Fark kayboldu: Bu kadar basit bir toplamayı derleyici ikisinde de aynı hıza getirebildi. Ama döngünün içi karmaşıklaşınca bu yardıma güvenemezsin. İki ders bir arada: Bellek sırası önemlidir ve ölçmeden "şu kesin yavaştır" denemez.

Aynı fikir yapılar için de geçerlidir. 16 alanlı yapının tek alanını gezmek, öteki 15 alanı da önbelleğe çeker:

```rust
use std::hint::black_box;
use std::time::Instant;

#[derive(Clone)]
struct Particle {
    x: f32,
    other: [f32; 15],
}

const COUNT: usize = 5_000_000;

fn main() {
    let together = vec![Particle { x: 1.0, other: [0.0; 15] }; COUNT];
    let only_x = vec![1.0f32; COUNT];

    let start = Instant::now();
    let sum: f32 = together.iter().map(|p| p.x).sum();
    black_box(sum);
    println!("together: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let sum: f32 = only_x.iter().sum();
    black_box(sum);
    println!("separate: {} ms", start.elapsed().as_millis());
    black_box(&together[0].other);
}
```

```text
together: 16 ms
separate: 4 ms
```

Bu düzene **SoA** (struct of arrays, dizilerden yapı) denir. Her zaman doğru değildir: Bir öğenin bütün alanlarıyla çalışıyorsan yapı dizisi daha iyidir. İşin hangi alanlara dokunduğuna bak.

## Iterator yavaş mı?

```rust
use std::hint::black_box;
use std::time::Instant;

fn main() {
    let values = black_box(vec![1u64; 50_000_000]);

    let start = Instant::now();
    let mut sum = 0u64;
    for i in 0..values.len() {
        sum += values[i];
    }
    black_box(sum);
    println!("index: {} ms", start.elapsed().as_millis());

    let start = Instant::now();
    let sum: u64 = values.iter().sum();
    black_box(sum);
    println!("iterator: {} ms", start.elapsed().as_millis());
}
```

```text
index: 24 ms
iterator: 23 ms
```

Hayır. Iterator eniyilemeden sonra elle yazılmış döngü kadar hızlıdır, çoğu zaman sınır denetimini de kaldırır. Okunabilir olanı yaz, ölçmeden "hızlı" olana çevirme.

## Önce algoritma

Bütün bunlar sabit çarpanlardır. O(n²)'lik algoritmayı hiçbir önbellek numarası kurtarmaz. Sıra şudur: Ölç, algoritmaya bak, sonra ayırmalar, en son düzen. Hedefe ulaşınca dur; okunamaz hâle gelen kod da bir maliyettir.

## Özet

- Yalnızca `--release` ölç; `black_box` işin silinmesini önler.
- Zaman sıcak bölgededir; ölçmeden iyileştirme yapma.
- `with_capacity`, yeniden kullanılan tampon, ödünç alma, `Cow`.
- `Box` büyük varyantı küçültür; `Option<Box<T>>` bedavadır.
- Bellek sırasında gez, tek alan için ayrı dizileri düşün.
- Önce algoritma.
