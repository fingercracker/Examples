
fn experiment1() {
// #############################################################################
    // DEBUG TRAIT
    /* 
        Any type can derive the debug trait of std::fmt. This is not true, for example,
        for fmt::Display -- if Display is not implemented, then we have to add a custom
        implementation for it.
     */
    // This object can't be printed at all.
    #[allow(dead_code)]
    struct UnPrintable(i32);

    // This struct can be printed using debug
    #[allow(dead_code)]
    #[derive(Debug)]
    struct DebugPrintable(i32);
    let thing = DebugPrintable(10);
    println!("{thing:?}");
}

fn experiment2() {
    #[allow(dead_code)]
    #[derive(Debug)]
    struct Space(i32);

    #[allow(dead_code)]
    #[derive(Debug)]
    struct Deep(Space);

    println!("We can print {:?}", Space(8));

    println!("We can also print {:?}", Deep(Space(9)));
}

fn main() {
    experiment1();
    experiment2();
}