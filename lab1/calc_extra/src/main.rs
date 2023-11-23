use calc_extra::lexer::lexer;
use calc_extra::parser::parse;
use std::io::{stdout, BufRead, Write};

pub fn main() {
    print!("input expr: ");
    stdout().flush();
    let stdin = std::io::stdin();
    for line in stdin.lock().lines() {
        println!("{}", parse(lexer(line.unwrap())).unwrap().eval());
        print!("input expr: ");
        stdout().flush();
    }
}
