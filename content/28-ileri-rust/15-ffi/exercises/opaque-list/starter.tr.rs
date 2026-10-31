pub struct List {
    values: Vec<i32>,
}

// #[unsafe(no_mangle)] pub extern "C" fn list_new() -> *mut List ...
// #[unsafe(no_mangle)] pub unsafe extern "C" fn list_push(list: *mut List, value: i32) ...
// #[unsafe(no_mangle)] pub unsafe extern "C" fn list_sum(list: *const List) -> i32 ...
// #[unsafe(no_mangle)] pub unsafe extern "C" fn list_free(list: *mut List) ...

fn main() {
    let list = list_new();
    unsafe {
        list_push(list, 2);
        list_push(list, 3);
        println!("{}", list_sum(list));
        list_free(list);
    }
}
