use std::fmt;
use std::ops::{Add, Div, Mul, Rem, Sub};

#[derive(Debug)]
pub enum Token<T>
where
    T: PartialEq
        + Add<Output = T>
        + Sub<Output = T>
        + Mul<Output = T>
        + Div<Output = T>
        + Rem<Output = T>
        + fmt::Debug
        + Copy,
{
    Num(T),
    Add,
    Minus,
    Multi,
    Div,
    LeftPar,
    RightPar,
}

#[derive(PartialEq)]
enum State {
    Num,
    Add,
    Minus,
    Multi,
    Div,
    LeftPar,
    RightPar,
}

fn str_2_token(s: &String, state: &State) -> Token<i32> {
    match &state {
        State::Num => match s.parse::<i32>() {
            Ok(n) => Token::Num(n),
            _ => Token::Num(0),
        },
        _ => {
            todo!()
        }
    }
}

pub fn lexer<S: Into<String>>(expr: S) -> Vec<Token<i32>> {
    let mut tokens = vec![];
    let mut curr = String::new();
    let mut prev_state = State::Num;

    for c in expr.into().chars() {
        match c {
            d @ '0'..='9' => {
                if prev_state != State::Num {
                    tokens.push(str_2_token(&curr, &prev_state));
                    curr = String::new();
                }
                prev_state = State::Num;
                curr.push(d);
            }
            '+' => {
                prev_state = State::Add;
                tokens.push(Token::Add);
            }
            '-' => {
                prev_state = State::Minus;
                tokens.push(Token::Minus);
            }
            '*' => {
                prev_state = State::Multi;
                tokens.push(Token::Multi);
            }
            '/' => {
                prev_state = State::Div;
                tokens.push(Token::Div);
            }
            '(' => {
                prev_state = State::LeftPar;
                tokens.push(Token::LeftPar);
            }
            ')' => {
                prev_state = State::RightPar;
                tokens.push(Token::RightPar);
            }
            _ => {
                todo!()
            }
        }
    }
    tokens
}

#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test_lexer() {
        println!("{:#?}", lexer("123"))
    }
}
