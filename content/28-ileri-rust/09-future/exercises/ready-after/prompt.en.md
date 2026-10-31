Write `Future` for `ReadyAfter`. If `left` is zero, return `Ready(value)`. Otherwise decrease `left`, tell the waker and return `Pending`.
