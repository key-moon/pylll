from typing import List, overload

from pylll.fpfloat import FPFloat
from pylll.lll import reduce
from pylll.utils import mul

def poly_mul(f: List[int], g: List[int]):
  res = [0] * (len(f) + len(g) - 1)
  for i, fi in enumerate(f):
    for j, gi in enumerate(g):
      res[i + j] += fi * gi
  return res

@overload
def evaluate(f: List[int], x: FPFloat) -> FPFloat: ...
@overload
def evaluate(f: List[int], x: int) -> int: ...
def evaluate(f, x):
  return sum([x**i * coeff for i, coeff in enumerate(f)], FPFloat(0) if isinstance(x, FPFloat) else 0)

NEWTON_ITER = 1000
def root(f: List[int], x_0: FPFloat):
  f_prime = [i * coeff for i, coeff in list(enumerate(f))[1:]]
  x = x_0
  for _ in range(NEWTON_ITER):
    x -= evaluate(f, x) / evaluate(f_prime, x)
  return x

def coppersmith(f: List[int], n: int, x_max: int, pow_num=3, shift_num=2):
  f_degree = len(f) - 1
  max_degree = f_degree * pow_num + shift_num

  f_pow = [[1]]
  for i in range(pow_num):
    f_pow.append(poly_mul(f, f_pow[-1]))

  lattice = []
  for i in range(pow_num+1):
    mul(f_pow[i], n**(pow_num - i))
    for shift in range(shift_num+1):
      g = [0] * shift + f_pow[i]
      g += [0] * ((max_degree + 1) - len(g))
      assert len(g) == max_degree + 1
      for j in range(len(g)):
        g[j] *= x_max**j
      lattice.append(g)

  reduce(lattice)

  res = []
  polys = [[coeff // (x_max**i) for i, coeff in enumerate(row)] for row in lattice]
  for poly in polys:
    while len(poly) and poly[-1] == 0: poly.pop()
    while len(poly) and poly[0] == 0: poly.pop(0)
    if len(poly) <= 1: continue

    # TODO: this did not yields all possible roots
    x = int(root(poly, FPFloat(x_max)))
    if evaluate(f, x) % n == 0 and x not in res:
      res.append(x)
  return res
