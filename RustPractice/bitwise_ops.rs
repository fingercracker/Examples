fn main() {
    let x = 0b0011u32;
    let y = 0b0110u32;
    println!("bitwise AND of 0110 and 0011: {:04b}", x & y);
    println!("biwtise OR of 0110 and 0011: {:04b}", x | y);
    println!("bitwise XOR of 0110 and 0011: {:04b}", x ^ y);
    println!("bitshift 1 << 5: {}", 1 << 5);
    println!("bitshift 1 >> 5: {}", 1 >> 5);
}