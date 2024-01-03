use crate::*;

#[derive(PartialEq, Clone, Copy)]
enum Existence {
    Exist,
    None,
}

fn n_queen_task<const N: usize>(i: i32) -> i32
where
    [(); 2 * N - 1]:,
{
    let mut col_m = [Existence::None; N];
    let mut diag_m = [Existence::None; 2 * N - 1];
    let mut anti_diag_m = [Existence::None; 2 * N - 1];

    fn _dfs<const N: usize>(
        x: i32,
        y: i32,
        col_m: &mut [Existence; N],
        diag_m: &mut [Existence; 2 * N - 1],
        anti_diag_m: &mut [Existence; 2 * N - 1],
    ) -> i32 {
        if x >= N as i32 {
            if y == 0 {
                return 1;
            };
            return 0;
        }

        let _y = y as usize;
        let _diag = (x - y + N as i32 - 1) as usize;
        let _anti_diag = (x + y) as usize;

        if col_m[_y] != Existence::None
            || diag_m[_diag] != Existence::None
            || anti_diag_m[_anti_diag] != Existence::None
        {
            return 0;
        }

        let mut cnt = 0;
        col_m[_y] = Existence::Exist;
        diag_m[_diag] = Existence::Exist;
        anti_diag_m[_anti_diag] = Existence::Exist;
        for _y in 0..N as i32 {
            cnt += _dfs(x + 1, _y, col_m, diag_m, anti_diag_m);
        }
        anti_diag_m[_anti_diag] = Existence::None;
        diag_m[_diag] = Existence::None;
        col_m[_y] = Existence::None;
        cnt
    }

    _dfs(0, i, &mut col_m, &mut diag_m, &mut anti_diag_m)
}

pub(crate) fn n_queen<const N: usize>() -> i32
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
        let res = crate::flag::n_queen::<$time>();
        println!("{res}");
    };
}

pub(crate) use test_n_queen;
