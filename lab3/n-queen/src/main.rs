#![allow(unused_macros, dead_code, incomplete_features, unused_imports)]
#![feature(generic_const_exprs)]

pub(crate) use rayon::iter::*;

mod bitop;
mod flag;

fn main() {
    // bitop::test_n_queen_bit!(16);
    bitop::test_n_queen_bit!(18);
    // flag::test_n_queen!(16);
    // n_queen::<32>();
}
