`Timer::new(ms)`: Paylaşılan durumu kur, kol açıp `ms` kadar uyu, `done`'ı doğru yap ve varsa waker'ı uyandır. `poll`: `done` ise `Ready`, değilse son waker'ı sakla ve `Pending`.
