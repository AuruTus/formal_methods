use crate::lexer::{self, *};
use core::fmt::Debug;
use std::vec;

pub trait Expr<Output: Numeric> {
    fn etype(&self) -> String;
    fn eval(&self) -> Output;
}

impl<N: Numeric> Debug for dyn Expr<N> {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "{}", self.etype())
    }
}

macro_rules! impl_binary_op {
    ($t: ident, $op: tt) => {
        impl<N: Numeric + 'static> $t<N> {
            pub fn default() -> Self {
                Self {
                    left: Box::new(Num(Default::default())),
                    right: Box::new(Num(Default::default())),
                }
            }

            pub fn new(left: Box<dyn Expr<N>>, right: Box<dyn Expr<N>>) -> Self {
                Self{
                    left,
                    right,
                }
            }
        }

        impl<N: Numeric> Expr<N> for $t<N> {
            fn etype(&self) -> String {
                format!("{{{}: {:?} {:?}}}", stringify!($t), self.left, self.right)
            }
            fn eval(&self) -> N {
                self.left.eval() $op self.right.eval()
            }
        }
    };
}

#[derive(Debug)]
struct Num<N: Numeric>(N);

impl<N: Numeric> Expr<N> for Num<N> {
    fn etype(&self) -> String {
        format!("{{Num: {:?}}}", self.0)
    }
    fn eval(&self) -> N {
        self.0
    }
}

#[derive(Debug)]
struct Add<N: Numeric> {
    left: Box<dyn Expr<N>>,
    right: Box<dyn Expr<N>>,
}
impl_binary_op!(Add, +);

#[derive(Debug)]
struct Minus<N: Numeric> {
    left: Box<dyn Expr<N>>,
    right: Box<dyn Expr<N>>,
}
impl_binary_op!(Minus, -);

#[derive(Debug)]
struct Multi<N: Numeric> {
    left: Box<dyn Expr<N>>,
    right: Box<dyn Expr<N>>,
}
impl_binary_op!(Multi, *);

#[derive(Debug)]
struct Div<N: Numeric> {
    left: Box<dyn Expr<N>>,
    right: Box<dyn Expr<N>>,
}
impl_binary_op!(Div, /);

#[derive(Debug)]
struct Par<N: Numeric> {
    inner: Box<dyn Expr<N>>,
}

impl<N: Numeric + 'static> Par<N> {
    pub fn default() -> Self {
        Par {
            inner: Box::new(Num(Default::default())),
        }
    }
    pub fn new(inner: Box<dyn Expr<N>>) -> Self {
        Par { inner }
    }
}

impl<N: Numeric> Expr<N> for Par<N> {
    fn etype(&self) -> String {
        format!("({:?})", self.inner)
    }
    fn eval(&self) -> N {
        self.inner.eval()
    }
}

struct Root<N: Numeric> {
    child: Option<Box<dyn Expr<N>>>,
}

impl<N: Numeric> Root<N> {
    pub fn new() -> Self {
        Root { child: None }
    }
}

impl<N: Numeric> Expr<N> for Root<N> {
    fn etype(&self) -> String {
        match &self.child {
            Some(c) => format!("{{Root: {:?}}}", c),
            None => String::from("{{Root: None}}"),
        }
    }

    fn eval(&self) -> N {
        match &self.child {
            Some(e) => e.eval(),
            None => {
                panic!("empty root!")
            }
        }
    }
}

fn token_2_node<N: Numeric + 'static>(
    t: lexer::Token<N>,
    lf_nds: &mut Vec<Box<dyn Expr<N>>>,
) -> Box<dyn Expr<N>> {
    match t {
        lexer::Token::Add => {
            let right = lf_nds.pop().unwrap();
            let left = lf_nds.pop().unwrap();
            Box::new(Add::new(left, right))
        }
        lexer::Token::Minus => {
            let right = lf_nds.pop().unwrap();
            let left = lf_nds.pop().unwrap();
            Box::new(Minus::new(left, right))
        }
        lexer::Token::Multi => {
            let right = lf_nds.pop().unwrap();
            let left = lf_nds.pop().unwrap();
            Box::new(Multi::new(left, right))
        }
        lexer::Token::Div => {
            let right = lf_nds.pop().unwrap();
            let left = lf_nds.pop().unwrap();
            Box::new(Div::new(left, right))
        }
        lexer::Token::LeftPar => {
            let inner = lf_nds.pop().unwrap();
            Box::new(Par::new(inner))
        }
        lexer::Token::RightPar | lexer::Token::Num(_) => {
            panic!("token should not be in the stack")
        }
    }
}

fn parse<N: Numeric + 'static>(tokens: Vec<Token<N>>) -> Option<Box<dyn Expr<N>>> {
    let mut lf_nds: Vec<Box<dyn Expr<N>>> = vec![];
    let mut non_lf_nds: Vec<Token<N>> = vec![];
    let mut root = Box::new(Root::new());

    for t in tokens {
        match t {
            Token::Num(n) => {
                lf_nds.push(Box::new(Num(n)));
            }
            Token::Add | Token::Minus | Token::Multi | Token::Div => {
                while let Some(prev) = non_lf_nds.last() {
                    if prev.order() < 0 || prev.order() > 0 && prev.order() < t.order() {
                        break;
                    }
                    let prev = non_lf_nds.pop().unwrap();
                    let prev = token_2_node(prev, &mut lf_nds);
                    lf_nds.push(prev);
                }
                non_lf_nds.push(t);
            }
            Token::LeftPar => {
                non_lf_nds.push(t);
            }
            Token::RightPar => {
                while let Some(prev) = non_lf_nds.last() {
                    match prev {
                        Token::LeftPar => {
                            let prev = non_lf_nds.pop().unwrap();
                            let prev = token_2_node(prev, &mut lf_nds);
                            lf_nds.push(prev);
                            break;
                        }
                        _ => {
                            let prev = non_lf_nds.pop().unwrap();
                            let prev = token_2_node(prev, &mut lf_nds);
                            lf_nds.push(prev);
                        }
                    };
                }
            }
        }
    }

    while let Some(t) = non_lf_nds.last() {
        let prev = non_lf_nds.pop().unwrap();
        let prev = token_2_node(prev, &mut lf_nds);
        lf_nds.push(prev);
    }
    root.child = lf_nds.pop();
    Some(root)
}

#[cfg(test)]
mod test {
    use crate::{
        lexer::lexer,
        parser::{Add, Div, Expr, Minus, Multi, Num},
    };

    use super::parse;

    #[test]
    fn test_impl_macro_for_add() {
        let e = Add::new(
            Box::new(Num(1)),
            Box::new(Add::new(Box::new(Num(2)), Box::new(Num(0)))),
        );
        assert_eq!(1 + 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_minus() {
        let e = Minus::new(Box::new(Num(1)), Box::new(Num(2)));
        assert_eq!(1 - 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_multi() {
        let e = Multi::new(Box::new(Num(1)), Box::new(Num(2)));
        assert_eq!(1 * 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_div() {
        let e = Div::new(Box::new(Num(1)), Box::new(Num(2)));
        assert_eq!(1 / 2, e.eval());
    }

    #[test]
    fn test_parse() {
        macro_rules! _gen_ast_test {
            ($e: expr) => {
                let ast = parse::<i32>(lexer(stringify!($e))).unwrap();
                // println!("{:?}", ast);
                assert_eq!($e, ast.eval());
            };
        }
        _gen_ast_test!(1 + 1 + 2 - 3 * 2 + (2 * 3));
        _gen_ast_test!((2) + ((3 * 2) * 3 - 2));
        _gen_ast_test!(-1 + 1);
        _gen_ast_test!(-1 + 1 + (-2) * (-3 + (-8)));
    }
}
