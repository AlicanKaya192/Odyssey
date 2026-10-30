`trait Light { fn next(self: Box<Self>) -> Box<dyn Light>; fn color(&self) -> String; }` yaz; `Red` ve `Green` birbirine geçsin (`red`, `green`).
