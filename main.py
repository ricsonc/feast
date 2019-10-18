from feast import macros, h, curry, range2
from macropy.quick_lambda import macros, f
from ipdb import set_trace as st
from operator import *
from math import sqrt, ceil

M = 100

# "normal" python style
# could be made nicer with some comprehensions, but that's not the point

total = 0
for k in range(M):
    if k > 1:
        for j in range(2, 1 + int(sqrt(k))):
            if k % j == 0:
                break
        else:
            total += k
print total

# "functional" python, not really idiomatic

maxfac = lambda k: 1 + int(sqrt(k))
prime = lambda k: k > 1 and 0 not in [k % x for x in range(2, maxfac(k))]
print sum((x for x in range(M) if prime(x)))

# functional style with FEAST

with h:
    maxfac = f[1 + (int& sqrt^ _)]
    L.prime[k : k > 1 and 0 not in map/ (mod/k) ^ {2 >> maxfac/k}]
    print sum ^ filter/ prime/ {M}
