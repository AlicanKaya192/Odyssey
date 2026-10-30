Write `fn counter(step: u32) -> impl FnMut() -> u32`: on each call the total grows by `step` and the new total returns (the first call gives `step`).
