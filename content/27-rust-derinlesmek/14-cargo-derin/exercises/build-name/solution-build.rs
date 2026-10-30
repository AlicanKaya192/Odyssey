fn main() {
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rustc-env=RELEASE_NAME=spring");
}
