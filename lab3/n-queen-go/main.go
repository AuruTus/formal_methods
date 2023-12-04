package main

import (
	"fmt"
	"sync"
)

const N = 32

func n_queen_partial(x, y int) int {
	cnt := 0
	board := [N]int{}
	col_m := [N]int8{}
	diag_m := [2*N - 1]int8{}
	anti_diag_m := [2*N - 1]int8{}

	for i := range board {
		board[i] = -1
	}

	var dfs func(x, y int)
	dfs = func(x, y int) {
		if x >= N {
			if y == 0 {
				cnt++
			}
			return
		}
		if col_m[y] != 0 {
			return
		}
		if diag_m[x-y+N-1] != 0 {
			return
		}
		if anti_diag_m[x+y] != 0 {
			return
		}
		board[x] = y
		col_m[y] = 1
		diag_m[x-y+N-1] = 1
		anti_diag_m[x+y] = 1
		for _y := range [N]struct{}{} {
			dfs(x+1, _y)
		}
		anti_diag_m[x+y] = 0
		diag_m[x-y+N-1] = 0
		col_m[y] = 0
		board[x] = -1
	}

	dfs(x, y)
	return cnt
}

func main() {
	cnt_arr := [N]int{}
	cnt := 0
	wa := sync.WaitGroup{}

	for i := range [N]struct{}{} {
		wa.Add(1)
		i := i
		go func() {
			cnt_arr[i] = n_queen_partial(0, i)
			wa.Done()
		}()
	}
	wa.Wait()
	for _, c := range cnt_arr {
		cnt += c
	}
	fmt.Printf("%d\n", cnt)
}
