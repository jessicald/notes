# Class vs. Dictionary; or, An Example of Space–Time Tradeoff in Python

## Conclusions; or, tl;dr

### What wins?
* `struct`-like objects, i.e. ones that are largely the same as a C `struct` instance, win in the memory department.
    * These tests do not try to determine what is best for *very* large sets of values, however; I direct the reader to <http://stackoverflow.com/a/2670191> for an insight into that scenario when using a dictionary.
* Dictionaries beat out objects in access times.
    * According to [Wikipedia](https://en.wikipedia.org/wiki/Hash_table#In_programming_languages), the Python dictionary is highly optimised because it is used internally to implement namespaces. [[*citation needed*](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed)]

### Other notes
* `struct`-like objects are apparently easier on memory than dictionaries but are slightly slower to access. They can both serve the exact same purpose, and objects can return their fields as a dictionary with `object.__dict__`.
* `getattr()` and `setattr()` are slower on objects than the namespace operator.
* `get()` and `update()` are slower on dictionaries than the index operator.
    * `dict.update({key: value})` is so much slower than `dict[key] = value` that it should **only** be used for updating an existing dictionary with the values in another one. It's simply too expensive for adding or reassigning individual keys.
* `update()` seems to expand the hash table of a dictionary more conservatively than other methods of key/value creation, including explicitly making a new dictionary with the exact same entries as another.
* A class definition takes a considerably higher amount of memory compared to instances of a class. For example, the `dict` class clocks in at 800 bytes in these tests while the empty dictionary `{}` only takes 280 bytes. Of course, a definition only has to be loaded once.

## Definitions
* class: a Python class.
* object: an instance of a class.
* field: an instance variable of an object; can interchangably refer to a variable and its associated value, or a variable by itself.
* dictionary: an instance of Python's `dict` class, which is an implementation of a hash table.
* entry: a key/value pair in a hash table.
* method:
    1. a function bound to an object.
    2. an unbound function that accepts an object as (ideally) its first parameter.
* operator:
    * index: `[]`
    * namespace: `.`
    * assignment: `=`
* gender.py (derived from code in [colons/pyfoot/4caf837/conf.py](https://github.com/colons/pyfoot/blob/4caf837cf8d934cc7a57949ee8b2be37fe54d83a/conf.py#L63)):

```python
class GenderPronouns():
    def __init__(self,
            nom='xe',  # Nominative: she, he, it
            obl='xem',  # Oblique: her, him, it
            pos_det='xyr',  # Possessive, determiner: her, his, its
            pos_pro='xyrs',  # Possessive, predicate: hers, his, its
            reflex='xem'  # Reflexive: herself, himself, itself
            ):
        self.nom = nom
        self.obl = obl
        self.pos_det = pos_det
        self.pos_pro = pos_pro
        self.reflex = reflex
```

## Speed (Time) Tests

### Accessing an existing value

#### Fastest: Accessing a dictionary value through the index operator
```bash
$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}" "string = 'blah blah ' + pnoun['obl'] + ' blah blah'"

1000000 loops, best of 3: 0.419 usec per loop
```

#### Faster: Accessing an object field through the namespace operator
```bash
$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "string = 'blah blah ' + pnoun.obl + ' blah blah'"

1000000 loops, best of 3: 0.446 usec per loop
```

#### Slower: Accessing a dictionary value through the get() method
```bash
$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}" "string = 'blah blah ' + pnoun.get('obl') + ' blah blah'"

1000000 loops, best of 3: 0.637 usec per loop
```

#### Slowest: Accessing an object field through getattr()
```bash
$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "string = 'blah blah ' + getattr(pnoun, 'obl') + ' blah blah'"

1000000 loops, best of 3: 0.731 usec per loop
```


### Adding a new field or entry
The relative speeds also hold true for changing the value of an existing field or key.

#### Fastest: Adding a new entry in an existing dictionary through the assignment and index operators
The first test times the creation of a new dictionary from a copy of the original and the reassignment of a variable that holds it.

This is subtracted from the next test, which recreates and reassigns the dictionary each time to make sure we're always adding a *new* entry to the dictionary.

```bash
$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}; pnoun2 = pnoun.copy()" "pnoun = pnoun2.copy()"

1000000 loops, best of 3: 0.431 usec per loop

$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}; pnoun2 = pnoun.copy()" "pnoun['foo'] = 'a sizeable string'; pnoun = pnoun2.copy()"

1000000 loops, best of 3: 0.957 usec per loop
```
`~0.957 - ~0.431 = ~0.526 usec per loop.`

#### Faster: Adding a new field to an existing object through the namespace operator
The first test times the creation of a GenderPronouns object and the reassignment of a variable that holds one.

This is subtracted from the next test, which recreates and reassigns the object each time to make sure we're always adding a *new* field to the object.

```bash
$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')"

100000 loops, best of 3: 2.17 usec per loop

$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "pnoun.foo = 'a sizeable string'; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')"

100000 loops, best of 3: 2.9 usec per loop
```
`~2.9 - ~2.17 = 0.73 usec per loop.`

#### Slower: Adding a new field to an existing object through setattr()

```bash
$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "setattr(pnoun, 'foo', 'a sizeable string'); pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')"

100000 loops, best of 3: 3.12 usec per loop
```
`~3.12 - ~2.17 = ~0.95 usec per loop.`

#### Slowest: Adding a new entry in an existing dictionary through the update() method

```bash
$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}; pnoun2 = pnoun.copy()" "pnoun.update({'foo': 'a sizeable string'}); pnoun = pnoun2.copy()"

100000 loops, best of 3: 2.03 usec per loop
```
`~2.03 - ~0.431 = ~1.599 usec per loop.`


## Memory (Space) Tests
The following tests were performed in the Python 3.2 interpreter.

The order has been edited for clarity, but the values are unchanged.

### Set it up and show that the internal values are the same
```python
>>> from gender import GenderPronouns
>>> pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')
>>> pnoun2 = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}
>>> pnoun.__dict__ == pnoun2
True
```

### Use getsizeof() to measure the size of objects in octets (8-bit bytes)
getsizeof() shows the size of the object only, i.e. it does not include the sizes of the accompanying fields, keys, or values.

It will however account for the size of a dictionary's hash table.

```python
>>> from sys import getsizeof
...
>>> getsizeof(getsizeof)
72
>>> getsizeof(GenderPronouns)
832
>>> getsizeof(GenderPronouns())
64
>>> getsizeof(dict)
800
>>> getsizeof({})
280
>>> getsizeof(pnoun)
64
>>> getsizeof(pnoun2)
280
```

#### Adding one field to the original class
```python
>>> class GenderPronouns2():
...     def __init__(self,
...             nom='xe',
...             obl='xem',
...             pos_det='xyr',
...             pos_pro='xyrs',
...             reflex='xem',
...             foo='a sizeable string'
...             ):
...         self.nom = nom
...         self.obl = obl
...         self.pos_det = pos_det
...         self.pos_pro = pos_pro
...         self.reflex = reflex
...         self.foo = foo
...
>>> getsizeof(GenderPronouns2())
64
```

#### Adding two fields to the original class
```python
>>> class GenderPronouns2():
...     def __init__(self,
...             nom='xe',
...             obl='xem',
...             pos_det='xyr',
...             pos_pro='xyrs',
...             reflex='xem',
...             foo='a sizeable string',
...             key='value'
...             ):
...         self.nom = nom
...         self.obl = obl
...         self.pos_det = pos_det
...         self.pos_pro = pos_pro
...         self.reflex = reflex
...         self.foo = foo
...         self.key = key
...
>>> getsizeof(GenderPronouns2())
64
```

#### Adding one entry to the original dictionary
```python
>>> pnoun3 = pnoun2.copy()
>>> pnoun3.update({'foo': 'a sizeable string'})
>>> getsizeof(pnoun3)
664
>>> pnoun3 = pnoun3.copy()
>>> getsizeof(pnoun3)
664
```

##### update()ing seems to be kinder to the hash table than creating a completely new dict object
```python
>>> pnoun3
{'nom': 'she', 'obl': 'her', 'pos_pro': 'hers', 'foo': 'a sizeable string', 'reflex': 'herself', 'pos_det': 'her'}
>>> pnoun3 = {'nom': 'she', 'obl': 'her', 'pos_pro': 'hers', 'foo': 'a sizeable string', 'reflex': 'herself', 'pos_det': 'her'}
>>> getsizeof(pnoun3)
1048
```

#### Adding two entrys to the original dictionary
```python
>>> pnoun3 = pnoun2.copy()
>>> pnoun3.update({'foo': 'a sizeable string'})
>>> pnoun3.update({'key': 'value'})
>>> getsizeof(pnoun3)
664
>>> pnoun3
{'nom': 'she', 'obl': 'her', 'pos_pro': 'hers', 'key': 'value', 'foo': 'a sizeable string', 'reflex': 'herself', 'pos_det': 'her'}
>>> pnoun3 = {'nom': 'she', 'obl': 'her', 'pos_pro': 'hers', 'key': 'value', 'foo': 'a sizeable string', 'reflex': 'herself', 'pos_det': 'her'}
>>> getsizeof(pnoun3)
1048
```

##### update()ing is also kinder than creating a new entry via the assignment operator
```python
>>> pnoun3 = pnoun2.copy()
>>> getsizeof(pnoun3)
280
>>> pnoun3['foo'] = 'a sizeable string'
>>> getsizeof(pnoun3)
1048
```
