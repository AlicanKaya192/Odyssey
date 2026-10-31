`ReadyAfter` için `Future` yaz. `left` sıfırsa `Ready(value)` döndür. Değilse `left`'i azalt, waker'a haber ver ve `Pending` döndür.
