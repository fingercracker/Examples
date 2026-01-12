fn main() {
    // ###### Basic String Formatting

    // it'd December right now, so let's display the number of days
    println!("December has {} days", 31);

    // add two areguments, and reference them mutliple times...
    println!("We have two animals, a {0} and a {1}. The {1} loves the {0}. The {0} definitely does not love the {1}", "cat", "dog");

    // we can also use named arguments instead of positional arguments.
    println!("I like long walks on the {forest},
            gentle strolls on the {ocean},
            and long boat rides on the {city}",
            forest="forest",
            ocean="ocean",
            city="city");

    // inline formatting
    let x: u32 = 123456789;
    println!("base 10: {}", x);    // decimal
    println!("base 2:  {:b}", x);  // binary
    println!("base 8:  {:o}", x);  // octal
    println!("base 16: {:x}", x);  // hexidecimal

    // right justify and pad with spaces
    println!("{number:>5}", number=1);

    // we can also pad with zeros
    println!("{number:0>5}", number=1);

    // we can also left justify and do the same stuff
    println!("{number:0<5}", number=1); // prints 10000

    // we can also use variables in the specifier
    println!("{number:0<width$}", number=1, width=5);

    // BROKEN
    /*
        The rust compiler is smart, and catches that the incorrect number of
        arguments are being passed. 

        The error thrown is the following
        ```
            error: invalid reference to positional argument 1 (there is 1 argument)
        ```
    */
    // uncomment the following line to see the failure
    // println!("{0} and {1} forms 'we'", "you");

    // the compiler will warn against unused modules. But we can use a macro to override this
    // much like in C++. In Rust, evidently we do the following
    #[allow(dead_code)]
    struct Structure(i32);

    /* 
        By default, user defined modules do not implement fmt::Display, which is what is required
        in order to call macros such as println!, print!, etc...

        This is pretty interesting actually. The object itself is responsible for implementing an 
        abstract method from the fmt namespace in order to instruct the caller how it should be displayed.
        Basically a default formatter needs to be implemented by an object in order to print that object.

        The following commented out println call raises
        ```
            error[E0277]: `Structure` doesn't implement `std::fmt::Display`
        ```
    */
    // println!("Out unimplemented struct object won't print... {}", Structure(3));

    /* 
        We can also use predefined variables to capture in offsets when justifying strings.
    */
    let width: usize = 5;
    let number: f64 = 1.0;
    println!("{number:>width$}"); // prints "    1"

    /* we can control the number of decimal places when we print */
    let pi = 3.141592;
    let prec = 3;
    println!("The number PI = {pi} to {prec} digits of precision is {pi:.prec$}");
    println!("{0} to {1} digits of precision is {pi:.1$}", pi, prec);
}