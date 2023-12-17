from typing import Union

FloatLike = Union["FPFloat", int, float]

# Fixed Precision
PRECISION = 2**600
class FPFloat:
  data: int
  def __init__(self, n: Union[int, float], raw=False) -> None:
    self.data = int(n if raw else n * PRECISION)
  def __int__(self):
    return (self.data + (PRECISION // 2)) // PRECISION
  def __abs__(self):
    return FPFloat(abs(self.data), raw=True)
  def __add__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return FPFloat(self.data + other.data, raw=True)
    else:
      return FPFloat(self.data + other * PRECISION, raw=True)
  def __rsub__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return FPFloat(other.data - self.data, raw=True)
    else:
      return FPFloat(other * PRECISION - self.data, raw=True)
  def __sub__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return FPFloat(self.data - other.data, raw=True)
    else:
      return FPFloat(self.data - other * PRECISION, raw=True)
  def __mul__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return FPFloat((self.data * other.data) // PRECISION, raw=True)
    else:
      return FPFloat(self.data * other, raw=True)
  def __truediv__(self, other: "FPFloat"):
    return FPFloat(self.data // other.data) + FPFloat((self.data % other.data * PRECISION) // other.data, raw=True)
  def __le__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return self.data <= other.data
    else:
      return self.data <= (other * PRECISION)
  def __ge__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return self.data >= other.data
    else:
      return self.data >= (other * PRECISION)
  def __eq__(self, other: FloatLike):
    if isinstance(other, FPFloat):
      return self.data == other.data
    else:
      return self.data == (other * PRECISION)
  def __pow__(self, other: int):
    res = FPFloat(1)
    for _ in range(other):
      res *= self
    return res
