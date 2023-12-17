from typing import List, Union, overload
from pylll.fpfloat import FPFloat, FloatLike

@overload
def mul(vs: List[int], a: int): ...
@overload
def mul(vs: List[float], a: float): ...
def mul(vs, a):
  n = len(vs)
  for i in range(n):
    vs[i] *= a
 
@overload
def inner_product(vs: List[float], ws: List[float]) -> float: ...
@overload
def inner_product(vs: List[FPFloat], ws: Union[List[FPFloat], List[int], List[float]]) -> FPFloat: ...
def inner_product(vs, ws):
  n = len(vs)
  res = FPFloat(0) if isinstance(vs[0], FPFloat) else 0
  for i in range(n):
    res += vs[i] * ws[i]
  return res
 
@overload
def minus_with_coeff(vs: List[int], ws: List[int], coeff: int) -> None: ...
@overload
def minus_with_coeff(vs: List[float], ws: List[float], coeff: float) -> None: ...
@overload
def minus_with_coeff(vs: List[FPFloat], ws: List[FPFloat], coeff: FloatLike) -> None: ...
def minus_with_coeff(vs, ws, coeff):
  n = len(vs)
  for i in range(n):
    vs[i] -= ws[i] * coeff
