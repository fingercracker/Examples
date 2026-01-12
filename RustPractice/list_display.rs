use std::fmt;

struct List(Vec<i32>);

impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let vec = &self.0;

        write!(f, "[")?;

        for (index, v) in vec.iter().enumerate() {
            if index != 0 { write!(f, ", ")?;}
            write!(f, "{}: {}", index, v)?;
        }
        write!(f, "]")
    }
}

struct Color {
    r: u8,
    g: u8,
    b: u8
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let r_hex = format!("{:02X}", self.r);
        let g_hex = format!("{:02X}", self.g);
        let b_hex = format!("{:02X}", self.b);

        write!(f, "RGB ({}, {}, {}) 0x{}{}{}", self.r, self.g, self.b, r_hex, g_hex, b_hex)
    }
}

fn calculate_color(color: &Color) -> u32 {
    let red = color.r as u32;
    let green = color.g as u32;
    let blue = color.b as u32;

    return (red * 65_536) + (green * 256) + blue
}

fn main() {
    let v = List(vec![1, 2, 3]);
    println!("{}", v);

    let color = Color { r: 128, g: 255, b: 90 };
    println!("{}", color);

    let color2 = Color { r: 0, g: 200, b: 1 };
    println!("{color2}");

    let rgb_color = calculate_color(&color);
    let rgb_color2 = calculate_color(&color2);

    println!("RGB For Color : {rgb_color}");
    println!("RGB For Color2: {rgb_color2}");
}
