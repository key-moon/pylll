from typing import List
from pylll.fpfloat import FPFloat, PRECISION
from pylll.utils import inner_product, minus_with_coeff

def gram_schmidt(vs: List[List[int]]):
  n = len(vs)
  res: List[List[FPFloat]] = [[] for _ in range(n)]
  mus = [[FPFloat(0)] * n for _ in range(n)]
  norms = [FPFloat(0)] * n
  for i in range(n):
    res[i] = list(map(FPFloat, vs[i]))
    for j in range(i):
      if norms[j].data:
        mus[i][j] = inner_product(res[j], vs[i]) / norms[j]
        minus_with_coeff(res[i], res[j], mus[i][j])
    mus[i][i] = FPFloat(1)
    norms[i] = inner_product(res[i], res[i])
  return res, mus

def reduce_naive(bs: List[List[int]], delta: FPFloat = FPFloat(PRECISION // 4 * 3, raw=True)) -> None:
  n = len(bs)
  bstars, mus = gram_schmidt(bs)
  
  k = 1
  while k < n:
    for j in reversed(range(k)):
      mu_kj = mus[k][j]
      if abs(mu_kj) * 2 <= 1:
        continue
      q = int(mu_kj)
      minus_with_coeff(bs[k], bs[j], q)
      bstars, mus = gram_schmidt(bs)
    if inner_product(bstars[k], bstars[k]) >= (delta - mus[k][k - 1] ** 2) * inner_product(bstars[k - 1], bstars[k - 1]):
      k += 1
    else:
      bs[k], bs[k - 1] = bs[k - 1], bs[k]
      bstars, mus = gram_schmidt(bs)
      k = max(k - 1, 1)

def reduce(bs: List[List[int]], delta: FPFloat = FPFloat(PRECISION // 4 * 3, raw=True)) -> None:
  n = len(bs)
  bstars, mus = gram_schmidt(bs)
  norm_bstars = [inner_product(bstars[i], bstars[i]) for i in range(n)]

  k = 1
  while k < n:
    for j in reversed(range(k)):
      mu_kj = mus[k][j]
      if abs(mu_kj) * 2 <= 1:
        continue
      q = int(mu_kj)
      minus_with_coeff(bs[k], bs[j], q)
      minus_with_coeff(mus[k], mus[j], q)
      mus[k][j] = mu_kj - q
    if norm_bstars[k] >= (delta - mus[k][k - 1] ** 2) * norm_bstars[k-1]:
      k += 1
    else:
      bs[k], bs[k - 1] = bs[k - 1], bs[k]
      mup = mus[k][k - 1]
      B = norm_bstars[k] + mup ** 2 * norm_bstars[k - 1]
      mus[k][k - 1] = mup * norm_bstars[k - 1] / B
      norm_bstars[k] = norm_bstars[k] * norm_bstars[k - 1] / B
      norm_bstars[k - 1] = B
      for j in range(k - 1):
        mus[k - 1][j], mus[k][j] = mus[k][j], mus[k - 1][j]
      for j in range(k + 1, n):
        t = mus[j][k]
        mus[j][k] = mus[j][k - 1] - mup * t
        mus[j][k - 1] = t + mus[k][k - 1] * mus[j][k]
      k = max(k - 1, 1)
