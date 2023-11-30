#![feature(generic_const_exprs)]

fn n_queen<const N: usize>()
where
    [(); 2 * N - 1]:,
{
    let mut cnt: i128 = 0;
    let board = [-1; N];
    let col_m = [0 as i8; N];
    let diag_m = [0 as i8; 2 * N - 1];
    let anti_diag_m = [0 as i8; 2 * N - 1];

    fn _dfs<const N: usize>(
        x: i32,
        y: i32,
        cnt: &mut i128,
        mut board: [i32; N],
        mut col_m: [i8; N],
        mut diag_m: [i8; 2 * N - 1],
        mut anti_diag_m: [i8; 2 * N - 1],
    ) {
        if x >= N as i32 {
            if y == 0 {
                *cnt += 1;
            };
            return;
        }
        if col_m[y as usize] != 0 {
            return;
        }
        if diag_m[(x - y + N as i32 - 1) as usize] != 0 {
            return;
        }
        if anti_diag_m[(x + y) as usize] != 0 {
            return;
        }
        board[x as usize] = y;
        col_m[y as usize] = 1;
        diag_m[(x - y + N as i32 - 1) as usize] = 1;
        anti_diag_m[(x + y) as usize] = 1;
        for _y in 0..N as i32 {
            _dfs(x + 1, _y, cnt, board, col_m, diag_m, anti_diag_m);
        }
        anti_diag_m[(x + y) as usize] = 0;
        diag_m[(x - y + N as i32 - 1) as usize] = 0;
        col_m[y as usize] = 0;
        board[x as usize] = -1;
    }

    for y in 0..N as i32 {
        _dfs(0, y, &mut cnt, board, col_m, diag_m, anti_diag_m);
    }

    println!("{cnt}");
}

fn main() {
    n_queen::<32>();
}
