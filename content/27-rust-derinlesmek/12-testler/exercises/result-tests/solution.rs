fn parse_pair(text: &str) -> Result<(i32, i32), String> {
    let (a, b) = text.split_once(',').ok_or("no comma")?;
    let x = a.parse::<i32>().map_err(|_| "bad first")?;
    let y = b.parse::<i32>().map_err(|_| "bad second")?;
    Ok((x, y))
}

fn main() {
    println!("{:?}", parse_pair("1,2"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_a_pair() -> Result<(), String> {
        assert_eq!(parse_pair("1,2")?, (1, 2));
        Ok(())
    }

    #[test]
    fn no_comma() {
        assert_eq!(parse_pair("1"), Err(String::from("no comma")));
    }

    #[test]
    fn bad_parts() {
        assert_eq!(parse_pair("x,2"), Err(String::from("bad first")));
        assert_eq!(parse_pair("1,y"), Err(String::from("bad second")));
    }
}
