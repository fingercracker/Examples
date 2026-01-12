use std::fmt;

#[derive(Debug)]
struct Matrix(f32, f32, f32, f32);

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        return write!(f, "( {} {} )\n( {} {} )", self.0, self.1, self.2, self.3)
    }
}

fn transpose(mat: &Matrix) -> Matrix {
    let trans_mat = Matrix(mat.0, mat.2, mat.1, mat.3);
    return trans_mat
}

fn main() {
    let mat = Matrix(1.1, 1.2, 2.1, 2.2);
    println!("Matrix:\n{mat}");
    println!("Transposed Matrix:\n{}", transpose(&mat));
}
