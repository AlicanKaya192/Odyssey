Write `Drop` for `struct Log<'a> { lines: &'a mut Vec<String>, name: String }`: on deletion it adds `end <name>` to the list. `impl Drop for Log<'_>`.
