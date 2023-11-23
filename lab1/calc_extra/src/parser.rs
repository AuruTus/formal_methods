use std::marker::PhantomData;

use crate::lexer::*;

pub trait Expr<Output: Numeric> {
    fn eval(self) -> Output;
}

macro_rules! impl_binary_op {
    ($t: ident, $op: tt) => {
		impl<N: Numeric, E: Expr<N>> $t<E, N> {
			pub fn new(left: E, right: E) -> Self {
				$t{
					left,
					right,
					_phantom: Default::default(),
				}
			}
		}

        impl<N: Numeric, E: Expr<N>> Expr<N> for $t<E, N> {
            fn eval(self) -> N {
                self.left.eval() $op self.right.eval()
            }
        }
    };
}

#[derive(Debug)]
struct Num<N: Numeric>(N);

impl<N: Numeric> Expr<N> for Num<N> {
    fn eval(self) -> N {
        self.0
    }
}

#[derive(Debug)]
struct Add<E: Expr<N>, N: Numeric> {
    left: E,
    right: E,
    _phantom: PhantomData<N>,
}
impl_binary_op!(Add, +);

#[derive(Debug)]
struct Minus<E: Expr<N>, N: Numeric> {
    left: E,
    right: E,
    _phantom: PhantomData<N>,
}
impl_binary_op!(Minus, -);

#[derive(Debug)]
struct Multi<E: Expr<N>, N: Numeric> {
    left: E,
    right: E,
    _phantom: PhantomData<N>,
}
impl_binary_op!(Multi, *);

#[derive(Debug)]
struct Div<E: Expr<N>, N: Numeric> {
    left: E,
    right: E,
    _phantom: PhantomData<N>,
}
impl_binary_op!(Div, /);

#[derive(Debug)]
struct Par<E: Expr<N>, N: Numeric> {
    inner: E,
    _phantom: PhantomData<N>,
}

impl<N: Numeric, E: Expr<N>> Expr<N> for Par<E, N> {
    fn eval(self) -> N {
        self.inner.eval()
    }
}

// fn parse(tokens: Token<i32>) {}

#[cfg(test)]
mod test {
    use crate::parser::{Add, Div, Expr, Minus, Multi, Num};

    #[test]
    fn test_impl_macro_for_add() {
        let e = Add::new(Num(1), Num(2));
        assert_eq!(1 + 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_minus() {
        let e = Minus::new(Num(1), Num(2));
        assert_eq!(1 - 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_multi() {
        let e = Multi::new(Num(1), Num(2));
        assert_eq!(1 * 2, e.eval());
    }

    #[test]
    fn test_impl_macro_for_div() {
        let e = Div::new(Num(1), Num(2));
        assert_eq!(1 / 2, e.eval());
    }
}
