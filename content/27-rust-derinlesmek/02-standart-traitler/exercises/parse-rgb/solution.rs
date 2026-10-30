use std::str::FromStr;

#[derive(Debug, PartialEq)]
struct Rgb {
    r: u8,
    g: u8,
    b: u8,
}

impl FromStr for Rgb {
    type Err = String;

    fn from_str(text: &str) -> Result<Rgb, String> {
        let parts: Vec<&str> = text.split(',').collect();
        if parts.len() != 3 {
            return Err(String::from("need three parts"));
        }
        let r = parts[0].parse::<u8>().map_err(|_| "bad number")?;
        let g = parts[1].parse::<u8>().map_err(|_| "bad number")?;
        let b = parts[2].parse::<u8>().map_err(|_| "bad number")?;
        Ok(Rgb { r, g, b })
    }
}

fn main() {
    println!("{:?}", "1,2,3".parse::<Rgb>());
}
