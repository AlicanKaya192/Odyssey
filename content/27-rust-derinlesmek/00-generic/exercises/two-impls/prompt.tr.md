`struct Pair<T> { first: T, second: T }` yaz (`#[derive(Debug)]` ile). `swapped(self) -> Pair<T>` her tür için, `bigger(&self) -> T` yalnızca `T: PartialOrd + Copy` için olsun: İki ayrı `impl`.
