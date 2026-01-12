use std::fmt;

#[derive(Debug)]
struct PlanarPoint {
    x0: f64,
    x1: f64
}

impl fmt::Display for PlanarPoint {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "x0: {}, y0: {}", self.x0, self.x1)
    }
}

#[derive(Debug)]
struct ComplexNumber {
    real: f64,
    imag: f64
}

impl fmt::Display for ComplexNumber {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut imag_part = format!("+i{}", self.imag);
        if self.imag < 0.0 {
            imag_part = format!("-i{}", -1.0*self.imag)
        }
        write!(f, "{} {}", self.real, imag_part)
    }
}

fn main() {
    let point = PlanarPoint { x0: 1.2, x1: -11.5 };
    println!("Display: {point}");
    println!("Debug: {point:?}");

    let complex_point = ComplexNumber { real: 1.2, imag: -11.5 };
    let complex_point2 = ComplexNumber { real: -1.2, imag: 11.5 };
    println!("Display: {complex_point}");
    println!("Debug: {complex_point:?}");
    println!("Display: {complex_point2}");
    println!("Debug: {complex_point2:?}");
}
