use proc_macro::{Delimiter, Group, TokenStream, TokenTree};

#[proc_macro_attribute]
pub fn tag(args: TokenStream, item: TokenStream) -> TokenStream {
    let label = args.to_string();
    let mut tokens: Vec<TokenTree> = item.into_iter().collect();

    let mut iter = tokens.iter();
    let mut name = String::new();
    while let Some(token) = iter.next() {
        if token.to_string() == "fn" {
            name = iter.next().unwrap().to_string();
            break;
        }
    }

    let Some(TokenTree::Group(body)) = tokens.pop() else {
        panic!("tag works only on functions");
    };
    let mut new_body: TokenStream =
        format!("println!(\"[{label}] {name}\");").parse().unwrap();
    new_body.extend(body.stream());
    tokens.push(TokenTree::Group(Group::new(Delimiter::Brace, new_body)));
    tokens.into_iter().collect()
}
