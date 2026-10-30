`struct Wrapper(Vec<i32>)` için `Deref` yaz (`Target = Vec<i32>`). Böylece `w.len()` ve `w.first()` doğrudan çalışsın.
