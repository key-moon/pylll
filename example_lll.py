from typing import List

from pylll.lll import reduce
from pylll.utils import mul

P = 2**61-1
BASE = 13371337

def rolling_hash(l: List[int]):
  res = 0
  for i, item in enumerate(l):
    res += item * (BASE ** i)
    res %= P
  return res

target_hash = rolling_hash(list(b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'))

HASH_INF = 10**2
CONST_INF = 10**5

CHARACTOR = 15
CHARSET_MIDDLE = (ord("Z") + ord("A")) // 2

lattice = []
for i in range(CHARACTOR):
  row = [0] * CHARACTOR
  row[i] = 1
  row += [((BASE**i) % P) * HASH_INF] + [0]
  lattice.append(row)

const_row = [-CHARSET_MIDDLE] * CHARACTOR + [-target_hash * HASH_INF] + [CONST_INF]
lattice.append(const_row)
free_row = [0] * CHARACTOR + [P * HASH_INF] + [0]
lattice.append(free_row)

reduce(lattice)
for row in lattice:
  if row[-1] == 0: continue
  if row[-1] < 0: mul(row, -1)
  if row[-2] != 0:
    print(f"[!] not fully reduced ({row=})")
  collision = [item + CHARSET_MIDDLE for item in row[:CHARACTOR]]
  assert rolling_hash(collision) == target_hash, f'{rolling_hash(collision)=} {target_hash=}'
  print(f'[+] collision: {bytes(collision).decode()}')
  break
