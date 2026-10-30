`fn count_even(list: &[u32]) -> u32` yaz: Listeyi ikişerli parçalara ayır (`chunks(2)`), her parçayı `thread::scope` içinde ayrı kolda işle, çiftleri `AtomicU32` ile say. Kilit yok.
