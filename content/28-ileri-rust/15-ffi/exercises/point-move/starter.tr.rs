use std::ffi::c_int;

// #[repr(C)] struct Point { x: i32, y: i32 }
// #[unsafe(no_mangle)] unsafe extern "C" fn point_move(point: *mut Point, dx: i32, dy: i32) -> c_int ...

fn main() {
    let mut point = Point { x: 1, y: 2 };
    println!("{}", unsafe { point_move(&mut point, 2, 3) });
    println!("{} {}", point.x, point.y);
    println!("{}", unsafe { point_move(std::ptr::null_mut(), 2, 3) });
}
