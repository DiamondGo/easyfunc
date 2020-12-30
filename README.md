# Simple functional programming style for python

_Tested on python version *2.6*, *2.7*, *3.x*

This package provides an incomplete simulation of [LINQ](https://en.wikipedia.org/wiki/Language_Integrated_Query)/[Stream](https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html) style stream processing for python.

This package aims to provides but some convenient methods, not a complete fp toolset to replace traditional pythonic coding.

[TOC]

## Installation

### pip
> pip install easyfunc

## manually
Copy easyfunc.py to your project and use it.

## Usage

```python
from easyfunc import Stream
```

### Stream creating

Create from iterable
```python
Stream(range(10))
Stream([1,2,3,4,5])
```
Create Stream literally
```python
Stream.of(1,2,3,4)
```
Infinite number Stream
```python
Stream.number() # 0,1,2,3,...
Stream.number(start=100, step=5) # 100,105,110,...
```
Empty Stream
```python
Stream.empty()
```

### Stream combining

Concat with other Stream/Iterable
```python
Stream.concat(Stream.of(1,2,3), Stream.of(4,5,6)) # 1,2,3,4,5,6
Stream.concat(Stream.of(1,2,3), range(3)) # 1,2,3,0,1,2
```

Extend current Stream with Stream/Iterable
```python
Stream.of(1,2,3).extend(Stream.of(4,5,6)) # 1,2,3,4,5,6
Stream.of(1,2,3).extend(range(3)) # 1,2,3,0,1,2
```

Zip two Stream/Iterable
```python
Stream.zip(range(3), Stream.number()) # (0,0),(1,1),(2,2) # stop at the shorter one
Stream.number().zip_with(Stream.of(99, 100)) # (0,99),(0,100)
```

Append element(s) to current Stream
```python
Stream.of(1,2,3).append(4,5) # 1,2,3,4,5
```

Prepend element(s) to current Stream
```python
Stream.of(4,5).prepend(1,2,3) # 1,2,3,4,5
```

Flat inside iterable to one-dimension
```python
Stream.of([1,2,3], Stream.of(4,5,6)).flat() # 1,2,3,4,5,6
```

### Stream operating

Take from first
```python
Stream.number().take(4) # 0,1,2,3
Stream.number().take(4).take(5) # 0,1,2,3
```

Take while True, stop when False
```python
Stream.number().takeWhile(lambda x: x != 4) # 0,1,2,3
```

Filter by condition
```python
Stream.number().filter(lambda x: x % 2 == 0) # 0,2,4,6,...
```

### Element Accessing

Get next item
```python
Stream.number().next_item().get() # 0
Stream.empty().next_item().or_else(-1) # -1
```

Find first which satisfies
```python
Stream.number(start=1).find_first(lambda x: x % 6 == 0).or_else(100) # 6
```

### check elements

If any matchs
```python
Stream.number().take(8).any(lambda x: x % 7 == 0) # True
```

If all match
```python
Stream.of(2,4,6,8).all(lambda x: x % 2 == 0) # True
```

### map and foreach

Map each elements
```python
Stream.number().map(lambda x: str(x)) # '0','1','2',...
```

Foreach
```python
def printItem(x):
    print(x)
Stream.number().take(4).foreach(lambda x: printItem(x))
```

### aggregate operations

Sum for numbers
```python
Stream.number().take(10).sum() # 45
```

Join for strings
```python
Stream.number().map(lambda x: str(x)).take(4).join(".") # '0.1.2.3'
```

Fold(reduce)
```python
Stream.number().take(10).fold(lambda x, y: x+y, 0) # 45
```
