#[allow(dead_code)]

#[derive(Debug, Copy, Clone)] // so that we can create a copy of a pointer for a Point
struct Point {
    x: f32,
    y: f32
}

#[derive(Debug)]
struct Rectangle {
    top_left: Point,
    bottom_right: Point
}

fn calculate_area(r: &Rectangle) -> f32 {
    return (r.bottom_right.x - r.top_left.x) * (r.top_left.y - r.bottom_right.y)
}

fn square(top_left: &Point, d: &f32) -> Rectangle {
    return Rectangle { top_left: *top_left, bottom_right: Point { x: top_left.x + d, y: top_left.y - d}}
}

fn main() {
    let r = Rectangle { top_left: Point { x: 1.0, y: 3.0}, bottom_right: Point { x: 4.0, y: 1.0 } };
    let r_area = calculate_area(&r);
    println!("{r_area}");

    let s = square(&Point { x: 1.1, y: 4.3 }, &2.0);
    let s_area = calculate_area(&s);
    println!("The area of the square: {s_area}");
}
