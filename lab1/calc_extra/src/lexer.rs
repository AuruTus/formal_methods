pub use std::fmt;
pub use std::ops::{Add, Div, Mul, Rem, Sub};

pub trait Numeric:
    PartialEq
    + Add<Output = Self>
    + Sub<Output = Self>
    + Mul<Output = Self>
    + Div<Output = Self>
    + Rem<Output = Self>
    + fmt::Debug
    + Copy
{
}

impl<T> Numeric for T where
    T: PartialEq
        + Add<Output = Self>
        + Sub<Output = Self>
        + Mul<Output = Self>
        + Div<Output = Self>
        + Rem<Output = Self>
        + fmt::Debug
        + Copy
{
}

#[derive(Debug)]
pub enum Token<T: Numeric> {
    Num(T),
    Add,
    Minus,
    Multi,
    Div,
    LeftPar,
    RightPar,
}

fn str_2_token(s: &String) -> Token<i32> {
    match s.parse::<i32>() {
        Ok(n) => Token::Num(n),
        _ => Token::Num(0),
    }
}

pub fn lexer<S: Into<String>>(expr: S) -> Vec<Token<i32>> {
    let mut tokens = vec![];
    let mut curr = String::new();

    let push_num = |curr: &mut String, tokens: &mut Vec<Token<i32>>| {
        if curr.len() != 0 {
            tokens.push(str_2_token(&curr));
            *curr = String::new();
        }
    };

    for c in expr.into().chars() {
        match c {
            d @ '0'..='9' => {
                curr.push(d);
            }
            '+' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::Add);
            }
            '-' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::Minus);
            }
            '*' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::Multi);
            }
            '/' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::Div);
            }
            '(' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::LeftPar);
            }
            ')' => {
                push_num(&mut curr, &mut tokens);
                tokens.push(Token::RightPar);
            }
            _ => {
                push_num(&mut curr, &mut tokens);
                println!("unimplemented char: {} ascii: {}", c, c as i32);
            }
        }
    }
    push_num(&mut curr, &mut tokens);
    tokens
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_lexer() {
        println!("{:#?}", lexer("123 + * (((()"))
    }
}
