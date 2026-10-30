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

    // Result dönen bir test ve hata metinlerini deneyen testler yaz
}
