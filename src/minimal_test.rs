use p3_mersenne_31::Mersenne31;
use p3_field::{AbstractField, PrimeField32};
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

const N: usize = 16;
const LIMBS: usize = 6;
type F = Mersenne31;

#[derive(Clone, Copy, Debug)]
pub struct U8Integer<T> { pub inner: T }
impl<T: Default> Default for U8Integer<T> {
    fn default() -> Self { Self { inner: T::default() } }
}

#[derive(Clone, Copy, Debug)]
pub struct SafeBigUint8<T: Copy, const LIMBS: usize> {
    pub limbs: [U8Integer<T>; LIMBS],
}

#[derive(Clone, Copy, Debug)]
pub struct UnsafeBigUint8<T, const LIMBS: usize> {
    pub limbs: [U8Integer<T>; LIMBS],
}

pub struct UnsafeBigUint8DotProduct<T: Copy, const LIMBS: usize, const N: usize> {
    pub result: UnsafeBigUint8<T, 12>,
}

pub struct BigUint8DotProduct<T: Copy, const LIMBS: usize, const N: usize> {
    pub result: SafeBigUint8<T, 12>,
}

impl<F: PrimeField32, const LIMBS: usize, const N: usize> UnsafeBigUint8DotProduct<F, LIMBS, N> {
    pub fn populate(
        a: [SafeBigUint8<F, LIMBS>; N],
        b: [SafeBigUint8<F, LIMBS>; N],
        result: &mut UnsafeBigUint8DotProduct<F, LIMBS, N>,
    ) {
        result.result = UnsafeBigUint8 {
            limbs: core::array::from_fn(|_| U8Integer { inner: F::zero() }),
        };

        for (a_val, b_val) in a.iter().zip(b.iter()) {
            for i in 0..LIMBS {
                for j in 0..LIMBS {
                    if i + j < 12 {
                        let product = a_val.limbs[i].inner.as_canonical_u32() * b_val.limbs[j].inner.as_canonical_u32();
                        let current = result.result.limbs[i + j].inner.as_canonical_u32();
                        result.result.limbs[i + j].inner = F::from_canonical_u32(current + product);
                    }
                }
            }
        }
    }
}

impl<F: PrimeField32, const LIMBS: usize, const N: usize> BigUint8DotProduct<F, LIMBS, N> {
    pub fn populate(
        a: [SafeBigUint8<F, LIMBS>; N],
        b: [SafeBigUint8<F, LIMBS>; N],
        result: &mut BigUint8DotProduct<F, LIMBS, N>,
    ) {
        result.result = SafeBigUint8 {
            limbs: core::array::from_fn(|_| U8Integer { inner: F::zero() }),
        };

        for (a_val, b_val) in a.iter().zip(b.iter()) {
            for i in 0..LIMBS {
                for j in 0..LIMBS {
                    if i + j < 12 {
                        let product = a_val.limbs[i].inner.as_canonical_u32() * b_val.limbs[j].inner.as_canonical_u32();
                        let current = result.result.limbs[i + j].inner.as_canonical_u32();
                        result.result.limbs[i + j].inner = F::from_canonical_u32(current + product);
                    }
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_unsafe_add_mul() {
        let mut rng = StdRng::seed_from_u64(42);
        let mut a = [0u64; N];
        let mut b = [0u64; N];

        for i in 0..N {
            a[i] = rng.gen::<u64>() & ((1 << 48) - 1);
            b[i] = rng.gen::<u64>() & ((1 << 48) - 1);
        }

        let a_big: Vec<_> = a.iter().map(|&x| {
            let mut limbs = [U8Integer { inner: F::zero() }; LIMBS];
            for i in 0..LIMBS {
                limbs[i].inner = F::from_canonical_u32(((x >> (8 * i)) & 0xFF) as u32);
            }
            SafeBigUint8 { limbs }
        }).collect();

        let b_big: Vec<_> = b.iter().map(|&x| {
            let mut limbs = [U8Integer { inner: F::zero() }; LIMBS];
            for i in 0..LIMBS {
                limbs[i].inner = F::from_canonical_u32(((x >> (8 * i)) & 0xFF) as u32);
            }
            SafeBigUint8 { limbs }
        }).collect();

        let a_array: [SafeBigUint8<F, LIMBS>; N] = a_big.try_into().unwrap();
        let b_array: [SafeBigUint8<F, LIMBS>; N] = b_big.try_into().unwrap();

        let mut dot_product = UnsafeBigUint8DotProduct {
            result: UnsafeBigUint8 { 
                limbs: core::array::from_fn(|_| U8Integer { inner: F::zero() })
            },
        };
        UnsafeBigUint8DotProduct::populate(a_array, b_array, &mut dot_product);

        let output = dot_product.result;

        let mut result: u128 = 0;
        for i in (0..12).rev() {
            result = result * 256 + output.limbs[i].inner.as_canonical_u32() as u128;
        }

        let expected: u128 = a.iter().zip(b.iter()).map(|(&x, &y)| (x as u128) * (y as u128)).sum();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_safe_add_mul() {
        let mut rng = StdRng::seed_from_u64(42);
        let mut a = [0u64; N];
        let mut b = [0u64; N];

        for i in 0..N {
            a[i] = rng.gen::<u64>() & ((1 << 48) - 1);
            b[i] = rng.gen::<u64>() & ((1 << 48) - 1);
        }

        let a_big: Vec<_> = a.iter().map(|&x| {
            let mut limbs = [U8Integer { inner: F::zero() }; LIMBS];
            for i in 0..LIMBS {
                limbs[i].inner = F::from_canonical_u32(((x >> (8 * i)) & 0xFF) as u32);
            }
            SafeBigUint8 { limbs }
        }).collect();

        let b_big: Vec<_> = b.iter().map(|&x| {
            let mut limbs = [U8Integer { inner: F::zero() }; LIMBS];
            for i in 0..LIMBS {
                limbs[i].inner = F::from_canonical_u32(((x >> (8 * i)) & 0xFF) as u32);
            }
            SafeBigUint8 { limbs }
        }).collect();

        let a_array: [SafeBigUint8<F, LIMBS>; N] = a_big.try_into().unwrap();
        let b_array: [SafeBigUint8<F, LIMBS>; N] = b_big.try_into().unwrap();

        let mut dot_product = BigUint8DotProduct {
            result: SafeBigUint8 { 
                limbs: core::array::from_fn(|_| U8Integer { inner: F::zero() })
            },
        };
        BigUint8DotProduct::populate(a_array, b_array, &mut dot_product);

        let output = dot_product.result;

        let mut result: u128 = 0;
        for i in (0..12).rev() {
            result = result * 256 + output.limbs[i].inner.as_canonical_u32() as u128;
        }

        let expected: u128 = a.iter().zip(b.iter()).map(|(&x, &y)| (x as u128) * (y as u128)).sum();

        assert_eq!(result, expected);
    }
}
