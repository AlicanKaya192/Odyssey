Write `trait Light { fn next(self: Box<Self>) -> Box<dyn Light>; fn color(&self) -> String; }`; `Red` and `Green` pass to each other (`red`, `green`).
