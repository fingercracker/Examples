use crate::List::*;

// linked list implementation via enums
#[derive(Debug)]
enum List {
    // value with a pointer to the next node
    Cons(u32, Box<List>),
    // end of the list
    Nil
}

impl List {
    fn new() -> List {
        Nil
    }

    fn prepend(self, elem: u32) -> List {
        // I am confused by what 'Box::new(self)' is doing here.
        Cons(elem, Box::new(self))
    }

    fn len(&self) -> u32 {
        match *self {
            Cons(_, ref tail) => 1 + tail.len(),
            Nil => 0
        }
    }

    fn stringify(&self) -> String {
        match *self {
            Cons(head, ref tail) => format!("{}, {}", head, tail.stringify()),
            Nil => format!("Nil")
        }
    }
}

enum Ops {
    Add,
    Subtract,
    Multiply
}

impl Ops {
    fn run(&self, x: f32, y: f32) -> f32 {
        match self {
            Self::Add => x + y,
            Self::Subtract => x - y,
            Self::Multiply => x * y
        }
    }
}

fn main() {
    // add the namespaces explicitly so that we don't have to keep doing so
    use crate::Ops::{Add, Subtract, Multiply};

    let adder = Add;
    let subtracter = Subtract;
    let mutliplier = Multiply;
    let x = 1.1234;
    let y = -189.1292;
    let add_res = adder.run(x, y);
    let sub_res = subtracter.run(x, y);
    let mult_res = mutliplier.run(x, y);
    println!("{add_res}");
    println!("{sub_res}");
    println!("{mult_res}");

    let mut list = List::new();

    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);

    println!("List has length {}", list.len());
    println!("List has elements: {}", list.stringify());
}
