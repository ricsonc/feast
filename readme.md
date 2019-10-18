### Functionally Enhanced Abstract Syntax Tree (FEAST)

This is a hack, which, with the help of the *macropy*  library, modifies the python AST at import time, with the idea of allowing for "nicer" functional programming in python.

Here, we show example code for computing the sum of prime numbers less than 100.

    M = 100

    L.maxfac[k : 1 + (int& sqrt^ k)]
    L.prime[k : k > 1 and 0 not in map/ f[mod(k, _)] ^ {2 >> maxfac/k}]
    print sum ^ filter/ prime/ {M}
	
    # is equivalent to the "normal" python syntax
    maxfac = lambda k: 1 + int(sqrt(k))
    prime = lambda k: k > 1 and 0 not in [k % x for x in range(2, maxfac(k))]
    print sum((x for x in range(M) if prime(x)))

1. currying: all functions are automatically curried
2. haskell style composition and application <br>
`&` is composition <br>
`^` is application (lower precedence than `&`) <br>
`/` is application (higher precedence than `&`) <br>
Examples: <br>
`f & g & h ^ x/ y/ z` <br>
is equivalent to the haskell syntax <br>
`f . g . h $ x y z` <br>
is equivalent to the python syntax <br>
`f(g(h(x(y)(z))))` <br>
3. nicer syntax for defining functions <br>
`L.foo[x : stuff]` <br>
is equivalent to <br>
`foo = lambda x: stuff` <br>
4. nicer syntax for creating lambdas (macropy feature, NOT mine) <br>
`f[_+2] ` <br>
is equivalent to <br>
`lambda x: x+2` <br>
5. nicer ranges 
```
{a >> b}
{N}
```
is equivalent to
```
range(a,b)
range(N)
```
