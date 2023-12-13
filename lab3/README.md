# Lab3 SAT

__Table of Contents__
- [Challenge](#challenge)

# Challenge

__Q__: How long does your program take to solve 8-queen?

__A__: Can see results in `8-queen.txt`. The Z3 costs `1.22s` to get all 92 results

__Q__: How long does your program take to solve 100-queens?

__A__: I don't know. There're too many results to iterate. It even costs me almost 5 hours to get the mere 6226 arrangements. I suppose it may take me years to find all answers with Z3.

__Q__: What's the maximal of N your program can solve?

__A__: I think Z3 version is less than 16-queen. I tried single thread in `Rust`, which cost `5m2.916s` for 16-queen, and multi-coroutines in Go with `0m31.752s`. I cannot get all results of 32-queen within 2 hours on my machine and the printout txt is really too large (`774.85MB`), so I give up rewriting a multi-thread Rust version. And it's not quite convenient to shard too many tasks on my poor 8 Hyper-threads CPU.
