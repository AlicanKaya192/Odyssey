use proc_macro::TokenStream;

#[proc_macro_derive(TypeName)]
pub fn type_name(input: TokenStream) -> TokenStream {
    let mut tokens = input.into_iter();
    let mut name = String::new();
    while let Some(token) = tokens.next() {
        let word = token.to_string();
        if word == "struct" || word == "enum" {
            name = tokens.next().unwrap().to_string();
            break;
        }
    }
    format!(
        "impl {name} {{
            fn type_name() -> &'static str {{
                {name:?}
            }}
        }}"
    )
    .parse()
    .unwrap()
}
