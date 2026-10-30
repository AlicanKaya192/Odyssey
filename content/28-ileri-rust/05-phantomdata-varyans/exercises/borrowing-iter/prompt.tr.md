`Iter<'a, T>` için `Iterator` yaz, `Item = &'a T`. `left` 0 ise `None`; yoksa `&*self.ptr`, işaretçiyi ilerlet, `left`'i azalt.
