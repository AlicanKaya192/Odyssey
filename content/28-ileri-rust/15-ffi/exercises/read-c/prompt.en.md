Write `read_c(pointer)`: `None` for a null pointer. Otherwise read with `CStr::from_ptr`, give a copy in `Some(String)` if it is valid UTF-8, otherwise `None`.
