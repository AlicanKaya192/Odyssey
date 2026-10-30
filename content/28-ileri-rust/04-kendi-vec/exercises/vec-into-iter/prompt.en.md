Write `IntoIterator`, `Iterator` and `Drop`. Wrap `MyVec` with `ManuallyDrop`; if the iterator stops half way the rest drop, and then memory is given back.
