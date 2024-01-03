use crate::*;

fn n_queen_task_bit<const N: usize>(i: u64) -> i32 {
    fn _dfs<const N: usize>(x: u64, y: u64, diag: u64, anti_diag: u64) -> i32 {
        let mut cnt = 0;
        let mut available = ((1 << N) - 1) & !(y | diag | anti_diag);
        while available != 0 {
            let p = available & (!available + 1);
            available ^= p;
            if x == (N - 1) as u64 {
                cnt += 1;
            } else {
                cnt += _dfs::<N>(x + 1, y | p, (diag | p) >> 1, (anti_diag | p) << 1);
            }
        }
        cnt
    }
    let p = 1 << i;
    _dfs::<N>(1, p, p >> 1, p << 1)
}

pub(crate) fn n_queen_bit<const N: usize>() -> i32
where
    [(); 2 * N - 1]:,
{
    (0..N)
        .into_par_iter()
        .map(|i| n_queen_task_bit::<N>(i as u64))
        .sum()
}

macro_rules! test_n_queen_bit {
    ($time:expr) => {
        let res = crate::bitop::n_queen_bit::<$time>();
        println!("{res}");
    };
}

pub(crate) use test_n_queen_bit;
