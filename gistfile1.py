$ python3.2 -mtimeit -s"from gender import GenderPronouns; pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')" "string = 'blah blah ' + pnoun.obl + ' blah blah'"
1000000 loops, best of 3: 0.446 usec per loop

$ python3.2 -mtimeit -s"pnoun = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}" "string = 'blah blah ' + pnoun['obl'] + ' blah blah'"
1000000 loops, best of 3: 0.419 usec per loop

$ python3.2
Python 3.2.3 (default, Apr 23 2012, 23:14:44) 
[GCC 4.7.0 20120414 (prerelease)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> # from gender import GenderPronouns
...
>>> class GenderPronouns():
...     def __init__(self,
...             nom='xe',
...             obl='xem',
...             pos_det='xyr',
...             pos_pro='xyrs',
...             reflex='xem'
...             ):
...         self.nom = nom
...         self.obl = obl
...         self.pos_det = pos_det
...         self.pos_pro = pos_pro
...         self.reflex = reflex
...
>>> pnoun = GenderPronouns('she', 'her', 'her', 'hers', 'herself')
>>> pnoun2 = {'nom': 'she', 'obl': 'her', 'pos_det': 'her', 'pos_pro': 'hers', 'reflex': 'herself'}
>>> pnoun.__dict__ == pnoun2
True
>>> from sys import getsizeof
>>> # Shows the size of the structure only, i.e. not with the sizes of the accompanying strings (or the size of the keys in the case of dictionaries, although it will account for the size of the hash table)
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