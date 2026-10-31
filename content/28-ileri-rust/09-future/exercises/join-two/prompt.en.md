Write `Future` for `Join2`, with the result `(u32, u32)`. On each poll, poll the unfinished ones, and never poll a finished one again. When both finish, `Ready((a, b))`.
