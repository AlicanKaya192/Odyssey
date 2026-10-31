use proc_macro::{Delimiter, Spacing, TokenStream, TokenTree};

#[proc_macro_derive(Show)]
pub fn show(input: TokenStream) -> TokenStream {
    let tokens: Vec<TokenTree> = input.into_iter().collect();

    let mut iter = tokens.iter();
    let mut name = String::new();
    while let Some(token) = iter.next() {
        if token.to_string() == "struct" {
            name = iter.next().unwrap().to_string();
            break;
        }
    }

    let body = tokens.iter().find_map(|token| match token {
        TokenTree::Group(group) if group.delimiter() == Delimiter::Brace => Some(group),
        _ => None,
    });
    let inner: Vec<TokenTree> = body.unwrap().stream().into_iter().collect();
    let fields: Vec<String> = inner
        .windows(2)
        .filter_map(|pair| match pair {
            [TokenTree::Ident(field), TokenTree::Punct(mark)]
                if mark.as_char() == ':' && mark.spacing() == Spacing::Alone =>
            {
                Some(field.to_string())
            }
            _ => None,
        })
        .collect();

    let parts: Vec<String> = fields.iter().map(|f| format!("{f}: {{:?}}")).collect();
    let args: Vec<String> = fields.iter().map(|f| format!("self.{f}")).collect();
    let text = format!("{name} {{{{ {} }}}}", parts.join(", "));
    format!(
        "impl {name} {{
            fn show(&self) -> String {{
                format!({text:?}, {})
            }}
        }}",
        args.join(", ")
    )
    .parse()
    .unwrap()
}
