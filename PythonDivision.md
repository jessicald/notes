Notes on Python division
========================

Multiplicative inverse, i.e. computing 1/*x* for a given *x*
--------------------------------------------------------
### Definitions
* multiplicative inverse: in mathematics, a multiplicative inverse or reciprocal for a number *x*, denoted by 1/*x* or *x*^-1, is a number which when multiplied by *x* yields the multiplicative identity, 1; the multiplicative inverse of a fraction *a*/*b* is *b*/*a*. [[1][c1]]

[c1]: https://en.wikipedia.org/wiki/Multiplicative_inverse

### In Python 3
If the numerator and denominator are known separately and *x* = num/dem, calculating dem/num is roughly 1.5 times faster than calculating 1/*x* and roughly twice as fast as calculating *x*^-1.

If the numerator and denominator are not known, 1/*x* is the fastest option. *x*^-1 should be avoided in this case.

#### Using denominator/numerator
```bash
$ python3.2 -mtimeit -s"num = 3; dem = 7; sup = num/dem" "dup = dem/num"

10000000 loops, best of 3: 0.17 usec per loop
```

#### Using 1/*x*
```bash
$ python3.2 -mtimeit -s"num = 3; dem = 7; sup = num/dem" "dup = 1/sup"

1000000 loops, best of 3: 0.276 usec per loop
```

#### Using *x*^-1
```bash
$ python3.2 -mtimeit -s"num = 3; dem = 7; sup = num/dem" "dup = sup**-1"

1000000 loops, best of 3: 0.364 usec per loop
```

### In Python 2
Python 2 has a nasty habit of returning an `int` as the result of dividing two `int`s, so additional calls to `float()` must be made to specify `float` division. `float()` is an *particularly* costly procedure.

This problem makes it necessary to tailor the code to the specific use case, which can be troublesome. The below tests assume you always want a `float` out of the inversion operation and that the number to invert is a `float`.

Below, using 1/*x* is faster **if the number to invert is already a** `float`; otherwise the fastest operation is, ironically, *x*^-1.

Also note that if you get `0` from a integer division that would be between `0.0` and `1.0` in a float division, your inversion will raise a `ZeroDivisionError`. That is why we always call `float()` on the first division.

#### Using denominator/numerator
```bash
$ python2.7 -mtimeit -s"num = 3; dem = 7; sup = float(num)/dem" "dup = float(dem)/num"

1000000 loops, best of 3: 0.48 usec per loop
```

#### Using 1/*x* with `float()` to make sure the result is a `float`
```bash
$ python2.7 -mtimeit -s"num = 3; dem = 7; sup = float(num)/dem" "dup = 1/float(sup)"

1000000 loops, best of 3: 0.594 usec per loop
```

#### Using 1/*x* assuming the number to invert is a `float`
```bash
$ python2.7 -mtimeit -s"num = 3; dem = 7; sup = float(num)/dem" "dup = 1/sup"

1000000 loops, best of 3: 0.216 usec per loop
```

#### Using *x*^-1 (always returns a `float`)
```bash
$ python2.7 -mtimeit -s"num = 3; dem = 7; sup = float(num)/dem" "dup = sup**-1"

1000000 loops, best of 3: 0.327 usec per loop
```

