use proc_macro::TokenStream;

#[proc_macro]
pub fn text_of(input: TokenStream) -> TokenStream {
    format!("{:?}", input.to_string()).parse().unwrap()
}
