// import fmt so we can use it in defining our custom display trait
use std::fmt;

struct Structure(i32, i32);

impl fmt::Display for Structure {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({0}, {1})", self.0, self.1)
    }
}

fn main() {
    let thing = Structure(10, 12);
    println!("This should work...: {thing}");
}
