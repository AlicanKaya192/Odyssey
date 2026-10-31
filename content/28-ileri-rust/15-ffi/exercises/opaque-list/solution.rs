pub struct List {
    values: Vec<i32>,
}

#[unsafe(no_mangle)]
pub extern "C" fn list_new() -> *mut List {
    Box::into_raw(Box::new(List { values: Vec::new() }))
}

/// # Safety
/// `list` must come from `list_new` and must not be freed yet.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn list_push(list: *mut List, value: i32) {
    let list = unsafe { &mut *list };
    list.values.push(value);
}

/// # Safety
/// `list` must come from `list_new` and must not be freed yet.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn list_sum(list: *const List) -> i32 {
    let list = unsafe { &*list };
    list.values.iter().sum()
}

/// # Safety
/// `list` must come from `list_new` and is invalid after this call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn list_free(list: *mut List) {
    if !list.is_null() {
        drop(unsafe { Box::from_raw(list) });
    }
}

fn main() {
    let list = list_new();
    unsafe {
        list_push(list, 2);
        list_push(list, 3);
        println!("{}", list_sum(list));
        list_free(list);
    }
}
