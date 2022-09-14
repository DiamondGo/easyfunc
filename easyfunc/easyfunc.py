import sys
from itertools import chain

# zip
try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

pyver = {
    (2, 6): "2",
    (2, 7): "2",
    (3, 4): "3",
    (3, 5): "3",
    (3, 6): "3",
    (3, 7): "3",
    (3, 8): "3",
    (3, 9): "3",
    (3, 10): "3",
    (3, 11): "3",
    (3, 12): "3"
}[(sys.version_info[0], sys.version_info[1])]


def iterable(obj):
        try:
            _ = iter(obj)
        except TypeError:
            return False
        else:
            return True


class Optional:
    def __init__(self, value, present=True):
        self.__empty = not present
        self.__val = value

    def get(self):
        if self.__empty:
            raise RuntimeError("Optional is empty")
        return self.__val

    def or_else(self, elseVal):
        return self.__val if not self.__empty else elseVal

    def if_present(self, elseVal):
        return not self.__empty

    def or_else_get(self, supplier):
        return self.__val if not self.__empty else supplier()

    @classmethod
    def of(cls, value):
        return cls(value)

    @classmethod
    def empty(cls):
        return cls(None, False)


class Stream:
    def __init__(self, it):
        self.__it = it
        self.__inner_iter = self.__it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        return {"3": self.__next__py3, "2": self.__next__py2}[pyver]()

    def __next__py2(self):
        return self.__inner_iter.next()

    def __next__py3(self):
        return self.__inner_iter.__next__()

    def next(self):
        return self.__next__()

    def next_item(self):
        try:
            return Optional.of(self.next())
        except StopIteration:
            return Optional.empty()

    def to_list(self):
        return list(self)

    def to_map(self, key=(lambda x: x[0]), value=(lambda y: y[1])):
        return { key(i) : value(i) for i in self }

    @classmethod
    def of(cls, *value):
        def gen():
            for item in value:
                yield item
        return cls(gen())

    @classmethod
    def empty(cls):
        return Stream([])

    @classmethod
    def number(cls, start=0, step=1):
        def gen():
            i = start
            while True:
                yield i
                i += step
        return cls(gen())

    def take(self, count):
        def gen():
            taken = 0
            while taken < count:
                try:
                    yield self.next()
                except StopIteration:
                    return
                taken = taken + 1
        return Stream(gen())

    def take_while(self, predictor):
        def gen():
            for item in self:
                if predictor(item):
                     yield item
                else:
                    break
        return Stream(gen())

    def filter(self, predictor):
        def gen():
            for item in self:
                if predictor(item):
                    yield item
        return Stream(gen())

    def map(self, maper):
        def gen():
            for item in self:
                yield maper(item)
        return Stream(gen())

    def foreach(self, consumer):
        for item in self:
            consumer(item)

    def any(self, predictor):
        for item in self:
            if predictor(item):
                return True
        return False

    def all(self, predictor):
        for item in self:
            if not predictor(item):
                return False
        return True

    def find_first(self, predictor):
        for item in self:
            if predictor(item):
                return Optional.of(item)
        return Optional.empty()

    @classmethod
    def concat(cls, *streams):
        return cls(chain(*streams))

    def extend(self, *streams):
        return Stream.concat(self, *streams)

    def append(self, *items):
        return self.extend(Stream.of(*items))

    def prepend(self, *items):
        return Stream.of(*items).extend(self)

    def flat(self):
        def gen():
            for item in self:
                for subitem in Stream(item):
                    yield subitem
        return Stream(gen())

    def fold(self, func, initial):
        cur = initial
        for item in self:
            cur = func(cur, item)
        return cur

    def sum(self):
        return self.fold(lambda x, y: x + y, 0)

    def join(self, sep):
        return sep.join(self)

    @classmethod
    def zip(cls, it1, it2):
        def gen():
            for i1, i2 in zip(it1, it2):
                yield i1, i2
        return cls(gen())

    def zip_with(self, it):
        return Stream.zip(self, it)

