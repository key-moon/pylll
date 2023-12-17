import random

from pylll.coppersmith import coppersmith

X_BITS = 256
MASK_BITS = X_BITS//3

m = random.randrange(2**(X_BITS - 1), 2**X_BITS)
x = random.randrange(m)

f_value = x**2 % m
x_upper = x // (2**MASK_BITS) * 2**MASK_BITS

# (lb+x)^2-f_value == x^2+2lb*x+lb^2-f_value
f = [(x_upper**2-f_value) % m, (2 * x_upper) % m, 1]
x_lower_cands = coppersmith(f, m, 2**MASK_BITS, pow_num=3, shift_num=1)

recovered_x = x_upper + x_lower_cands[0]

assert recovered_x == x
