`struct Log<'a> { lines: &'a mut Vec<String>, name: String }` için `Drop` yaz: Silinirken listeye `end <name>` eklesin. `impl Drop for Log<'_>`.
