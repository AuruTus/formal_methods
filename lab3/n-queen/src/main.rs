#![feature(generic_const_exprs)]

use rayon::iter::*;
use std::fmt::Error;

#[derive(PartialEq, Clone, Copy)]
enum Existence {
    Exist,
    None,
}

fn n_queen_task<const N: usize>(i: i32) -> i32
where
    [(); 2 * N - 1]:,
{
    let cnt = &mut 0;
    let col_m = [Existence::None; N];
    let diag_m = [Existence::None; 2 * N - 1];
    let anti_diag_m = [Existence::None; 2 * N - 1];

    fn _dfs<const N: usize>(
        x: i32,
        y: i32,
        cnt: &mut i32,
        mut col_m: [Existence; N],
        mut diag_m: [Existence; 2 * N - 1],
        mut anti_diag_m: [Existence; 2 * N - 1],
    ) {
        if x >= N as i32 {
            if y == 0 {
                *cnt += 1;
            };
            return;
        }

        let _y = y as usize;
        let _diag = (x - y + N as i32 - 1) as usize;
        let _anti_diag = (x + y) as usize;

        if col_m[_y] != Existence::None
            || diag_m[_diag] != Existence::None
            || anti_diag_m[_anti_diag] != Existence::None
        {
            return;
        }

        col_m[_y] = Existence::Exist;
        diag_m[_diag] = Existence::Exist;
        anti_diag_m[_anti_diag] = Existence::Exist;
        for _y in 0..N as i32 {
            _dfs(x + 1, _y, cnt, col_m, diag_m, anti_diag_m);
        }
        anti_diag_m[_anti_diag] = Existence::None;
        diag_m[_diag] = Existence::None;
        col_m[_y] = Existence::None;
    }

    _dfs(0, i, cnt, col_m, diag_m, anti_diag_m);

    *cnt
}

fn n_queen<const N: usize>() -> i32
where
    [(); 2 * N - 1]:,
{
    (0..N)
        .into_par_iter()
        .map(|i| n_queen_task::<N>(i as i32))
        .sum()
}

macro_rules! test_n_queen {
    ($time:expr) => {
        let res = n_queen::<$time>();
        println!("{res}");
    };
}

fn main() {
    test_n_queen!(16);
    // n_queen::<10>();
    // n_queen::<32>();
}
