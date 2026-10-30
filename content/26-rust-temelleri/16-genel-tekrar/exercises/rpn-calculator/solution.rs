fn eval(expr: &str) -> Result<i32, String> {
    let mut stack = Vec::new();
    for token in expr.split_whitespace() {
        match token {
            "+" | "-" | "*" => {
                let b = stack.pop().ok_or("too few values")?;
                let a = stack.pop().ok_or("too few values")?;
                stack.push(match token {
                    "+" => a + b,
                    "-" => a - b,
                    _ => a * b,
                });
            }
            _ => {
                let n = token.parse::<i32>().map_err(|_| format!("bad token: {token}"))?;
                stack.push(n);
            }
        }
    }
    if stack.len() != 1 {
        return Err(String::from("too many values"));
    }
    Ok(stack[0])
}

fn main() {
    println!("{:?}", eval("2 3 + 4 *"));
}
