import sys
from itertools import chain
pyver = {
    (2, 6): "2",
    (2, 7): "2",
    (3, 4): "3",
    (3, 5): "3",
    (3, 6): "3"
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

    def orElse(self, elseVal):
        return self.__val if not self.__empty else elseVal

    def ifPresent(self, elseVal):
        return not self.__empty

    def orElseGet(self, supplier):
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

    def tolist(self):
        return list(self)

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
                yield self.next()
                taken = taken + 1
        return Stream(gen())

    def takeWhile(self, predictor):
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

    def findFirst(self, predictor):
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





