import unittest

from func import pyver
from func import Optional
from func import Stream
from func import iterable


class TestFunc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testIterable(self):
        self.assertTrue(iterable([1, 2, 3]))
        self.assertTrue(iterable(range(3)))
        self.assertTrue(iterable("123"))
        self.assertFalse(iterable(123))

        def getNumber():
            i = 0
            while True:
                yield i
                i += 1
        self.assertTrue(iterable(getNumber()))

    def testOptional(self):
        empty = Optional.empty()
        self.assertRaises(RuntimeError, empty.get)
        self.assertEqual(3, empty.orElse(3))
        self.assertEqual(3, empty.orElseGet(lambda: 3))

        some = Optional.of("hello")
        self.assertEqual("hello", some.get())
        self.assertEqual("hello", some.orElse("world"))
        self.assertEqual("hello", some.orElseGet(lambda: 3))

    def testIterator(self):
        l = range(3)
        i = l.__iter__()

        def loop():
            while True:
                _ = i.__next__() if pyver == "3" else i.next()
        self.assertRaises(StopIteration, loop)

    def countIter(self, iter):
        return sum(1 for _ in iter)

    def testStreamBasic(self):
        s = Stream.of([1,2,3,4])
        self.assertEqual(4, self.countIter(s))

    def testInfinite(self):
        s = Stream.infinite(step=2)
        for i in range(100):
            self.assertEqual(i*2, s.next())

    def testTake(self):
        s = Stream.infinite(step=2)
        self.assertEqual(4, self.countIter(s.take(4)))
        self.assertEqual(0, self.countIter(s.take(0)))

    def testTakeWhile(self):
        self.assertEqual(8, self.countIter(Stream.infinite(step=2).takeWhile(lambda i: i < 15)))
        self.assertEqual(14, max(Stream.infinite(step=2).takeWhile(lambda i: i < 15)))
        self.assertEqual(0, max(Stream.infinite(step=2).takeWhile(lambda i: i < 1)))

    def testFilter(self):
        self.assertEqual(12, sum(Stream.infinite().filter(lambda i: i % 2 == 0).take(4)))

    def testTolist(self):
        self.assertEqual([1,3,5], Stream.infinite(start=1, step=2).take(3).tolist())

    def testMap(self):
        self.assertEqual(16, max(Stream.infinite().map(lambda x: x**2).take(5)));

    def testForeach(self):
        count = {"count":0}
        def addCount(x):
            count["count"] += x
        Stream.infinite().map(lambda x: x**2).filter(lambda x: x % 3 == 0).take(3).foreach(lambda x: addCount(x))
        self.assertEqual(45, count["count"])

    def testAnyAll(self):
        self.assertFalse(Stream.infinite(step=2).take(10).any(lambda x: x % 2 != 0))
        self.assertTrue(Stream.infinite(step=2).take(10).all(lambda x: x % 2 == 0))
        self.assertFalse(Stream.empty().any(lambda x: x > 0))
        self.assertTrue(Stream.empty().all(lambda x: x > 0))

    def testConcat(self):
        l = Stream.concat(Stream.infinite().filter(lambda i: i % 3 == 0).take(3),
                          Stream.infinite().filter(lambda i: i % 3 == 1).take(3),
                          Stream.infinite().filter(lambda i: i % 3 == 2).take(3)).tolist()
        self.assertEqual(9, len(l))
        self.assertEqual(8, l[-1])

    def testExtend(self):
        s = Stream.infinite().filter(lambda i: i % 3 == 0).take(3).extend(
            Stream.infinite().filter(lambda i: i % 3 == 1).take(3),
            Stream.infinite().filter(lambda i: i % 3 == 2).take(3))
        l = s.tolist()
        self.assertEqual(9, len(l))
        self.assertEqual(8, l[-1])





if __name__ == '__main__':
    unittest.main()