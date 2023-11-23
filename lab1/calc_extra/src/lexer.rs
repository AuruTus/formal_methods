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
    + Default
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
        + Default
        + Copy
{
}

#[derive(Debug, PartialEq, Eq)]
pub enum Token<T: Numeric> {
    Num(T),
    Add,
    Minus,
    Multi,
    Div,
    LeftPar,
    RightPar,
}

impl<T: Numeric> Token<T> {
    pub fn order(&self) -> i32 {
        match self {
            Self::Num(_) => 0,
            Self::Add | Self::Minus => 1,
            Self::Multi | Self::Div => 2,
            Self::LeftPar | Self::RightPar => -1,
        }
    }
}

fn str_2_num_token(s: &String, sgn: i32) -> Token<i32> {
    match s.parse::<i32>() {
        Ok(n) => Token::Num(sgn * n),
        _ => {
            panic!("invalid number string: {}", s);
        }
    }
}

pub fn lexer<S: Into<String>>(expr: S) -> Vec<Token<i32>> {
    let mut tokens = vec![];
    let mut curr = String::new();
    let mut par_cnt = 0;
    let mut sgn: i32 = 1;

    macro_rules! push_num {
        {} => {
            if curr.len() != 0 {
                tokens.push(str_2_num_token(&curr, sgn));
                curr = String::new();
                sgn = 1;
            }
        }
    }

    for c in expr.into().chars() {
        match c {
            d @ '0'..='9' => {
                curr.push(d);
            }
            '+' => {
                push_num!();
                tokens.push(Token::Add);
            }
            '-' => {
                match tokens.last() {
                    Some(t) => match t {
                        Token::Num(_) => {
                            push_num!();
                            tokens.push(Token::Minus);
                        }
                        Token::LeftPar => {
                            sgn = -1;
                        }
                        _ => {
                            panic!("invalid op \"-\" position")
                        }
                    },
                    None => {
                        sgn = -1;
                    }
                };
            }
            '*' => {
                push_num!();
                tokens.push(Token::Multi);
            }
            '/' => {
                push_num!();
                tokens.push(Token::Div);
            }
            '(' => {
                par_cnt += 1;
                push_num!();
                tokens.push(Token::LeftPar);
            }
            ')' => {
                par_cnt -= 1;
                push_num!();
                tokens.push(Token::RightPar);
            }
            ' ' => {
                push_num!();
            }
            _ => {
                panic!("unimplemented char: {} ascii: {}", c, c as i32)
            }
        }
    }
    if curr.len() != 0 {
        tokens.push(str_2_num_token(&curr, sgn));
    }
    if par_cnt != 0 {
        panic!("invalid parenthesis pairs")
    }
    tokens
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_lexer() {
        println!("{:#?}", lexer("123 + * ()"));
    }

    #[test]
    #[should_panic]
    fn test_lexer_parenthesis_panic() {
        lexer("1 + 2 + (((() + 3");
    }
}
