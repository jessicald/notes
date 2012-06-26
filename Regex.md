Regular Expressions for Various Languages
=========================================

Vim
---
### Replace any number of spaces after each period or colon in a line with a double space.
```
s/\([\.\:]\) \{-}\(\S\)/\1  \2/g
```

### Replace the beginning of each non-blank line with an indent of four spaces.
```
s/^\(.\)/    \1/
```
