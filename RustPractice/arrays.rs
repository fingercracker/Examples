use std::mem;

fn analyze_slice(slice: &[i32]) {
    println!("First element of the slice: {}", slice[0]);
    println!("Number of elements in the slice: {}", slice.len());
    println!("")
}

fn main() {
    let xs = [1, 2, 3, 4, 5];
    let ys: [i32; 500] = [0; 500];

    // Arrays are stack allocated.
    println!("Array occupies {} bytes\n", mem::size_of_val(&xs));

    println!("Analyse the whole array as a slice");
    analyze_slice(&xs);

    println!("Slice the first 10 elements of ys");
    analyze_slice(&ys[1..10]);

    for i in 0..xs.len() + 1 {
        match xs.get(i) {
            Some(xval) => println!("{}, {}", i, xval),
            None => println!("Whoops, {} is outside of the bounds of the array", i)
        }
    }
}
