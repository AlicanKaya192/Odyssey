`MyBox<T>`: `new` takes a pointer with `Box::into_raw`. Write `Deref`, `DerefMut` and `Drop`; `Drop` drops with `Box::from_raw`.
