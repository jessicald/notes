Regular Expressions for Various Languages
=========================================

Vim
---
### Replace any number of spaces after each period or colon with a double space.
```
%s/\([\.\:]\) \{-}\(\S\)/\1  \2/g
```
