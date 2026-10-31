use proc_macro::TokenStream;

#[proc_macro]
pub fn count_tokens(input: TokenStream) -> TokenStream {
    let count = input.into_iter().count();
    format!("{count}usize").parse().unwrap()
}
