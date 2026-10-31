Write `finishes_at_once`: fix the future with `pin!`, poll it once with `Waker::noop()`, and return `true` if `Ready` came. Do not require `Unpin` for `F`.
