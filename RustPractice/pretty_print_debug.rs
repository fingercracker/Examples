#[allow(dead_code)]
#[derive(Debug)]
struct Person<'a> {
    name: &'a str,
    age: u8
}

fn main() {
    let name = "John";
    let age = 39;
    let john = Person { name, age };

    println!("Regular Print: {john:?}");
    println!("Pretty Print: {john:#?}");
}