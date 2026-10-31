Write `Future` for `Select`. Poll `a` first; if it finishes, `Left(value)`. Then poll `b`; if it finishes, `Right(value)`. If neither finishes, `Pending`.
